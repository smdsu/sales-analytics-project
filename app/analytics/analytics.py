import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


async def get_gender_distribution(df: pd.DataFrame) -> plt.Figure:
    if 'gender' not in df.columns:
        raise ValueError("DataFrame должен содержать столбец 'gender'.")

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(
        data=df,
        x='gender',
        hue='gender',
        palette=['#d5a6bd', '#6fa8dc'],
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fontsize=12, padding=0)

    ax.set_title('Распределение пола клиентов', fontsize=16)
    ax.set_xlabel('Пол', fontsize=12)
    ax.set_ylabel('Количество', fontsize=12)
    plt.tight_layout()

    return fig
