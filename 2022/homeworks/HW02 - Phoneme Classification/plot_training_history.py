from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"


def main():
    history = pd.read_csv(RESULTS_DIR / "training_history.csv")
    epochs = history["epoch"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), dpi=160)

    axes[0].plot(
        epochs,
        history["train_loss"],
        color="#2563EB",
        marker="o",
        linewidth=2,
        label="Train",
    )
    axes[0].plot(
        epochs,
        history["valid_loss"],
        color="#D97706",
        marker="o",
        markerfacecolor="white",
        linestyle="--",
        linewidth=2,
        label="Validation",
    )
    axes[0].set_title("Cross-Entropy Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].grid(alpha=0.2)
    axes[0].legend(frameon=False)

    axes[1].plot(
        epochs,
        history["train_accuracy"] * 100,
        color="#2563EB",
        marker="o",
        linewidth=2,
        label="Train",
    )
    axes[1].plot(
        epochs,
        history["valid_accuracy"] * 100,
        color="#D97706",
        marker="o",
        markerfacecolor="white",
        linestyle="--",
        linewidth=2,
        label="Validation",
    )
    axes[1].set_title("Frame Classification Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy (%)")
    axes[1].grid(alpha=0.2)
    axes[1].legend(frameon=False)

    fig.suptitle(
        "HW02 Phoneme Classification - Training History",
        fontsize=14,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(
        RESULTS_DIR / "training_curves.png",
        bbox_inches="tight",
        facecolor="white",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
