import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"])

# Set date as index
df.set_index("date", inplace=True)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Copy data
    df_line = df.copy()

    # Create figure
    fig, ax = plt.subplots(figsize=(15, 5))

    # Draw line plot
    ax.plot(df_line.index, df_line["value"])

    # Labels and title
    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save and return image
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Copy and prepare data
    df_bar = df.copy()

    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Average daily page views for each month grouped by year
    df_bar = df_bar.groupby(
        ["year", "month"]
    )["value"].mean().unstack()

    # Create figure
    fig = df_bar.plot(
        kind="bar",
        figsize=(12, 8)
    ).figure

    # Labels
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")

    # Month labels
    plt.legend(
        title="Months",
        labels=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )

    # Save and return image
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Copy data
    df_box = df.copy()

    # Prepare data
    df_box.reset_index(inplace=True)

    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Create month order
    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    df_box["month"] = pd.Categorical(
        df_box["month"],
        categories=month_order,
        ordered=True
    )

    # Create figure with two plots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        x="month",
        y="value",
        data=df_box,
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save and return image
    fig.savefig("box_plot.png")
    return fig
