# ============================================================
# 1. 导入库
# ============================================================

import os
import gc
import random
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import TensorDataset, DataLoader


# ============================================================
# 2. 设置随机种子
# ============================================================

seed = 42

random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


# ============================================================
# 3. 设置设备
# ============================================================

device = torch.device(
    'cuda' if torch.cuda.is_available() else 'cpu'
)

print('使用设备：', device)

if torch.cuda.is_available():
    print('GPU：', torch.cuda.get_device_name(0))


# ============================================================
# 4. 设置路径和超参数
# ============================================================

data_dir = './libriphone/libriphone'

processed_dir = './processed_hw2'

results_dir = './results'

os.makedirs(
    results_dir,
    exist_ok=True
)

train_processed_dir = os.path.join(
    processed_dir,
    'train'
)

valid_processed_dir = os.path.join(
    processed_dir,
    'valid'
)

os.makedirs(
    train_processed_dir,
    exist_ok=True
)

os.makedirs(
    valid_processed_dir,
    exist_ok=True
)


# 前9帧 + 当前帧 + 后9帧
concat_nframes = 19

# 19 × 39 = 741
input_dim = concat_nframes * 39

# 41个类别
num_classes = 41


# 正式训练参数
batch_size = 1024

num_epochs = 10

learning_rate = 0.001

# 每100条语音保存成一个chunk
chunk_size = 100


# ============================================================
# 5. 读取 train_split.txt
# ============================================================

train_split_path = os.path.join(
    data_dir,
    'train_split.txt'
)

with open(train_split_path, 'r') as f:
    train_files = f.read().splitlines()


print('全部训练语音数量：', len(train_files))


# ============================================================
# 6. 读取 test_split.txt
# ============================================================

test_split_path = os.path.join(
    data_dir,
    'test_split.txt'
)

with open(test_split_path, 'r') as f:
    test_files = f.read().splitlines()


print('测试语音数量：', len(test_files))


# ============================================================
# 7. 读取 train_labels.txt
# ============================================================

train_labels_path = os.path.join(
    data_dir,
    'train_labels.txt'
)

with open(train_labels_path, 'r') as f:
    train_labels = f.read().splitlines()


# ============================================================
# 8. 建立标签字典
#
# 最终类似：
#
# label_dict['2007-149877-0023']
#
# 得到：
#
# [0, 0, 0, 29, 29, ...]
# ============================================================

label_dict = {}

for line in train_labels:

    parts = line.split()

    file_name = parts[0]

    labels = [
        int(label)
        for label in parts[1:]
    ]

    label_dict[file_name] = labels


print('标签字典语音数量：', len(label_dict))


# ============================================================
# 9. 按整条语音划分训练集和验证集
#
# 90%训练
# 10%验证
# ============================================================

all_train_files = train_files.copy()

random.shuffle(all_train_files)


valid_ratio = 0.1

valid_size = int(
    len(all_train_files) * valid_ratio
)


valid_files = all_train_files[:valid_size]

train_files_split = all_train_files[valid_size:]


print('训练语音数量：', len(train_files_split))
print('验证语音数量：', len(valid_files))


# ============================================================
# 10. 高效的前后帧拼接函数
#
# 输入：
# [帧数, 39]
#
# 输出：
# [帧数, 741]
# ============================================================

def concat_feat(x, concat_nframes=19):

    assert concat_nframes % 2 == 1

    half = concat_nframes // 2

    # x:
    # [T, 39]

    # 转成：
    # [1, 39, T]
    x = x.transpose(0, 1).unsqueeze(0)

    # 左右边界复制
    x = F.pad(
        x,
        pad=(half, half),
        mode='replicate'
    )

    # 变成：
    # [1, 39, T, 19]
    x = x.unfold(
        dimension=2,
        size=concat_nframes,
        step=1
    )

    # 变成：
    # [1, T, 19, 39]
    x = x.permute(
        0,
        2,
        3,
        1
    )

    # 最终：
    # [T, 741]
    x = x.reshape(
        x.shape[1],
        -1
    )

    return x.float()


# ============================================================
# 11. 读取一组训练语音
#
# 返回：
#
# X：[总帧数, 741]
# y：[总帧数]
# ============================================================

def load_train_data(file_list):

    all_features = []

    all_labels = []


    for file_name in file_list:

        feature_path = os.path.join(
            data_dir,
            'feat',
            'train',
            file_name + '.pt'
        )


        feature = torch.load(
            feature_path,
            map_location='cpu'
        )


        feature = concat_feat(
            feature,
            concat_nframes
        )


        labels = torch.tensor(
            label_dict[file_name],
            dtype=torch.long
        )


        assert feature.shape[0] == labels.shape[0]


        all_features.append(feature)

        all_labels.append(labels)


    X = torch.cat(
        all_features,
        dim=0
    )

    y = torch.cat(
        all_labels,
        dim=0
    )


    return X, y


# ============================================================
# 12. 分块预处理并保存
#
# 例如：
#
# train_000.pt
# train_001.pt
# ...
# ============================================================

def save_data_chunks(
    file_list,
    save_dir,
    prefix,
    chunk_size=100
):

    os.makedirs(
        save_dir,
        exist_ok=True
    )


    total_chunks = (
        len(file_list) + chunk_size - 1
    ) // chunk_size


    print()
    print('==============================')
    print(f'开始处理 {prefix}')
    print('语音数量：', len(file_list))
    print('chunk数量：', total_chunks)
    print('==============================')


    for chunk_idx in range(total_chunks):

        start = chunk_idx * chunk_size

        end = min(
            start + chunk_size,
            len(file_list)
        )


        save_path = os.path.join(
            save_dir,
            f'{prefix}_{chunk_idx:03d}.pt'
        )


        # 已经存在则跳过
        if os.path.exists(save_path):

            print(
                f'[{chunk_idx + 1}/{total_chunks}] '
                f'已存在，跳过：{save_path}'
            )

            continue


        chunk_files = file_list[start:end]


        print()
        print(
            f'[{chunk_idx + 1}/{total_chunks}] '
            f'正在处理语音 {start} ~ {end - 1}'
        )


        X, y = load_train_data(
            chunk_files
        )


        print('X：', X.shape)
        print('y：', y.shape)


        torch.save(
            {
                'X': X,
                'y': y
            },
            save_path
        )


        print('已保存：', save_path)


        del X
        del y

        gc.collect()


    print()
    print(f'{prefix} 全部处理完成！')


# ============================================================
# 13. 正式预处理训练集
#
# 第一次运行会花时间。
#
# 以后再次运行时，已经存在的chunk会自动跳过。
# ============================================================

save_data_chunks(
    file_list=train_files_split,
    save_dir=train_processed_dir,
    prefix='train',
    chunk_size=chunk_size
)


# ============================================================
# 14. 正式预处理验证集
# ============================================================

save_data_chunks(
    file_list=valid_files,
    save_dir=valid_processed_dir,
    prefix='valid',
    chunk_size=chunk_size
)


# ============================================================
# 15. 获取所有chunk文件
# ============================================================

train_chunk_files = sorted([
    os.path.join(
        train_processed_dir,
        file_name
    )
    for file_name in os.listdir(train_processed_dir)
    if file_name.endswith('.pt')
])


valid_chunk_files = sorted([
    os.path.join(
        valid_processed_dir,
        file_name
    )
    for file_name in os.listdir(valid_processed_dir)
    if file_name.endswith('.pt')
])


print('训练chunk数量：', len(train_chunk_files))
print('验证chunk数量：', len(valid_chunk_files))


# ============================================================
# 16. 定义模型
# ============================================================

class PhonemeModel(nn.Module):

    def __init__(self):

        super().__init__()


        self.model = nn.Sequential(

            nn.Linear(input_dim, 1024),

            nn.BatchNorm1d(1024),

            nn.ReLU(),

            nn.Dropout(0.2),


            nn.Linear(1024, 512),

            nn.BatchNorm1d(512),

            nn.ReLU(),

            nn.Dropout(0.2),


            nn.Linear(512, 256),

            nn.ReLU(),


            nn.Linear(256, num_classes)
        )


    def forward(self, x):

        return self.model(x)


model = PhonemeModel().to(device)


print(model)


# ============================================================
# 17. 损失函数和优化器
# ============================================================

criterion = nn.CrossEntropyLoss()


optimizer = torch.optim.Adam(
    model.parameters(),
    lr=learning_rate
)


# ============================================================
# 18. 保存训练记录
# ============================================================

train_losses = []

valid_losses = []

train_accuracies = []

valid_accuracies = []


best_valid_acc = 0.0


# ============================================================
# 19. 正式训练
# ============================================================

for epoch in range(num_epochs):

    print()
    print(
        f'================ Epoch '
        f'{epoch + 1}/{num_epochs} ================'
    )


    # --------------------------------------------------------
    # 训练
    # --------------------------------------------------------

    model.train()


    train_loss_sum = 0.0

    train_correct = 0

    train_total = 0


    # 每个epoch打乱chunk顺序
    random.shuffle(train_chunk_files)


    for chunk_index, chunk_path in enumerate(
        train_chunk_files
    ):

        chunk = torch.load(
            chunk_path,
            map_location='cpu'
        )


        X_chunk = chunk['X']

        y_chunk = chunk['y']


        chunk_dataset = TensorDataset(
            X_chunk,
            y_chunk
        )


        chunk_loader = DataLoader(
            chunk_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=0,
            pin_memory=True
        )


        for x_batch, y_batch in chunk_loader:

            x_batch = x_batch.to(
                device,
                non_blocking=True
            )

            y_batch = y_batch.to(
                device,
                non_blocking=True
            )


            optimizer.zero_grad()


            output = model(x_batch)


            loss = criterion(
                output,
                y_batch
            )


            loss.backward()


            optimizer.step()


            train_loss_sum += (
                loss.item()
                * x_batch.size(0)
            )


            pred = output.argmax(
                dim=1
            )


            train_correct += (
                pred == y_batch
            ).sum().item()


            train_total += y_batch.size(0)


        print(
            f'Train chunk '
            f'{chunk_index + 1}/{len(train_chunk_files)} '
            f'完成'
        )


        del chunk
        del X_chunk
        del y_chunk
        del chunk_dataset
        del chunk_loader

        gc.collect()


    train_loss = (
        train_loss_sum
        / train_total
    )


    train_acc = (
        train_correct
        / train_total
    )


    # --------------------------------------------------------
    # 验证
    # --------------------------------------------------------

    model.eval()


    valid_loss_sum = 0.0

    valid_correct = 0

    valid_total = 0


    with torch.no_grad():

        for chunk_index, chunk_path in enumerate(
            valid_chunk_files
        ):

            chunk = torch.load(
                chunk_path,
                map_location='cpu'
            )


            X_chunk = chunk['X']

            y_chunk = chunk['y']


            chunk_dataset = TensorDataset(
                X_chunk,
                y_chunk
            )


            chunk_loader = DataLoader(
                chunk_dataset,
                batch_size=batch_size,
                shuffle=False,
                num_workers=0,
                pin_memory=True
            )


            for x_batch, y_batch in chunk_loader:

                x_batch = x_batch.to(
                    device,
                    non_blocking=True
                )

                y_batch = y_batch.to(
                    device,
                    non_blocking=True
                )


                output = model(x_batch)


                loss = criterion(
                    output,
                    y_batch
                )


                valid_loss_sum += (
                    loss.item()
                    * x_batch.size(0)
                )


                pred = output.argmax(
                    dim=1
                )


                valid_correct += (
                    pred == y_batch
                ).sum().item()


                valid_total += y_batch.size(0)


            del chunk
            del X_chunk
            del y_chunk
            del chunk_dataset
            del chunk_loader

            gc.collect()


    valid_loss = (
        valid_loss_sum
        / valid_total
    )


    valid_acc = (
        valid_correct
        / valid_total
    )


    # --------------------------------------------------------
    # 保存记录
    # --------------------------------------------------------

    train_losses.append(train_loss)

    valid_losses.append(valid_loss)

    train_accuracies.append(train_acc)

    valid_accuracies.append(valid_acc)


    print()
    print(
        f'Epoch [{epoch + 1}/{num_epochs}]'
    )

    print(
        f'Train Loss: {train_loss:.4f}  '
        f'Train Accuracy: {train_acc:.4f}'
    )

    print(
        f'Valid Loss: {valid_loss:.4f}  '
        f'Valid Accuracy: {valid_acc:.4f}'
    )


    # --------------------------------------------------------
    # 保存最佳模型
    # --------------------------------------------------------

    if valid_acc > best_valid_acc:

        best_valid_acc = valid_acc


        torch.save(
            model.state_dict(),
            'best_model.pth'
        )


        print(
            f'保存最佳模型！'
            f'Valid Accuracy = {best_valid_acc:.4f}'
        )


print()
print('训练完成！')

print(
    '最佳验证准确率：',
    best_valid_acc
)


# ============================================================
# 20. 保存训练指标和效果图
# ============================================================

history = pd.DataFrame({
    'epoch': range(1, num_epochs + 1),
    'train_loss': train_losses,
    'valid_loss': valid_losses,
    'train_accuracy': train_accuracies,
    'valid_accuracy': valid_accuracies
})

history.to_csv(
    os.path.join(results_dir, 'training_history.csv'),
    index=False
)

with open(
    os.path.join(results_dir, 'metrics.json'),
    'w',
    encoding='utf-8'
) as f:
    json.dump(
        {
            'best_valid_accuracy': best_valid_acc,
            'epochs': num_epochs,
            'concat_nframes': concat_nframes,
            'input_dim': input_dim,
            'num_classes': num_classes
        },
        f,
        ensure_ascii=False,
        indent=2
    )

epochs = history['epoch']

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 4.8),
    dpi=160
)

axes[0].plot(
    epochs,
    history['train_loss'],
    color='#2563EB',
    marker='o',
    linewidth=2,
    label='Train'
)

axes[0].plot(
    epochs,
    history['valid_loss'],
    color='#D97706',
    marker='o',
    markerfacecolor='white',
    linestyle='--',
    linewidth=2,
    label='Validation'
)

axes[0].set_title('Cross-Entropy Loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].grid(alpha=0.2)
axes[0].legend(frameon=False)

axes[1].plot(
    epochs,
    history['train_accuracy'] * 100,
    color='#2563EB',
    marker='o',
    linewidth=2,
    label='Train'
)

axes[1].plot(
    epochs,
    history['valid_accuracy'] * 100,
    color='#D97706',
    marker='o',
    markerfacecolor='white',
    linestyle='--',
    linewidth=2,
    label='Validation'
)

axes[1].set_title('Frame Classification Accuracy')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy (%)')
axes[1].grid(alpha=0.2)
axes[1].legend(frameon=False)

fig.suptitle(
    'HW02 Phoneme Classification - Training History',
    fontsize=14,
    fontweight='bold'
)

fig.tight_layout()

figure_path = os.path.join(
    results_dir,
    'training_curves.png'
)

fig.savefig(
    figure_path,
    bbox_inches='tight',
    facecolor='white'
)

plt.close(fig)

print('训练记录已保存：', results_dir)
print('训练效果图已保存：', figure_path)


# ============================================================
# 21. 加载最佳模型
# ============================================================

model.load_state_dict(
    torch.load(
        'best_model.pth',
        map_location=device
    )
)

model.eval()


print('最佳模型加载完成！')


# ============================================================
# 22. 测试集预测
#
# 注意：
# test_split.txt中的顺序必须保持不变。
#
# 每一条测试语音：
#
# [帧数, 39]
#       ↓
# 前后19帧拼接
#       ↓
# [帧数, 741]
#       ↓
# 模型预测
# ============================================================

all_predictions = []


with torch.no_grad():

    for file_index, file_name in enumerate(
        test_files
    ):

        feature_path = os.path.join(
            data_dir,
            'feat',
            'test',
            file_name + '.pt'
        )


        feature = torch.load(
            feature_path,
            map_location='cpu'
        )


        feature = concat_feat(
            feature,
            concat_nframes
        )


        test_dataset = TensorDataset(
            feature
        )


        test_loader = DataLoader(
            test_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=0,
            pin_memory=True
        )


        for batch in test_loader:

            x_batch = batch[0].to(
                device,
                non_blocking=True
            )


            output = model(x_batch)


            pred = output.argmax(
                dim=1
            )


            all_predictions.extend(
                pred.cpu().tolist()
            )


        if (
            (file_index + 1) % 100 == 0
            or
            file_index + 1 == len(test_files)
        ):

            print(
                f'测试进度：'
                f'{file_index + 1}/{len(test_files)}'
            )


        del feature
        del test_dataset
        del test_loader

        gc.collect()


print()
print(
    '测试集预测总数：',
    len(all_predictions)
)


# ============================================================
# 23. 读取 sample_submission.csv
# ============================================================

sample_submission = pd.read_csv(
    './sample_submission.csv'
)


print(
    'sample_submission行数：',
    len(sample_submission)
)


# ============================================================
# 24. 检查预测数量
# ============================================================

assert (
    len(all_predictions)
    ==
    len(sample_submission)
), (
    f'预测数量不匹配！'
    f'预测：{len(all_predictions)}，'
    f'提交模板：{len(sample_submission)}'
)


# ============================================================
# 25. 写入预测结果
# ============================================================

submission = sample_submission.copy()


submission['Class'] = all_predictions


# ============================================================
# 26. 保存 submission.csv
# ============================================================

submission.to_csv(
    'submission.csv',
    index=False
)


print()
print('submission.csv 已成功生成！')

print(submission.head())

print(
    'submission形状：',
    submission.shape
)
