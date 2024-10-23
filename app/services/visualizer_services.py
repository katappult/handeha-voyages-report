import os

import matplotlib
from matplotlib import pyplot as plt

matplotlib.use('Agg')
import seaborn as sns


class DataVisualizer:
    @staticmethod
    def create_bar_chart(df, x_col, y_col, title):
        directory = os.path.join(os.getcwd(), 'diagram')

        if not os.path.exists(directory):
            os.makedirs(directory)

        output_path = os.path.join(directory, f"{title}.png")

        plt.figure(figsize=(15, 6))
        sns.barplot(x=x_col, y=y_col, data=df)
        plt.title(title)

        plt.savefig(output_path)
        plt.close()

        print(f"{title} Graph saved in: {output_path}")

    @staticmethod
    def create_pie_chart(df, column, count_column, title):
        directory = os.path.join(os.getcwd(), 'diagram')

        if not os.path.exists(directory):
            os.makedirs(directory)

        output_path = os.path.join(directory, f"{title}.png")

        plt.figure(figsize=(6, 6))
        # Use count_column for the pie chart values
        plt.pie(df[column], labels=df[count_column], autopct='%1.1f%%', startangle=140)
        plt.title(f"Distribution of {title}")
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the plot as an image file
        plt.savefig(output_path)
        plt.close()

        print(f"{title} Pie Chart saved in: {output_path}")

    @staticmethod
    def create_multi_line_chart(df, x_col, y_cols, title, colors):
        directory = os.path.join(os.getcwd(), 'diagram')

        if not os.path.exists(directory):
            os.makedirs(directory)

        output_path = os.path.join(directory, f"{title}.png")

        plt.figure(figsize=(15, 6))

        for i, y_col in enumerate(y_cols):
            plt.plot(df[x_col], df[y_col], label=y_col, color=colors[i])

        plt.title(title)
        plt.xlabel(x_col)
        plt.ylabel('Values')
        plt.legend()

        plt.savefig(output_path)
        plt.close()

        print(f"{title} Multi-Line Chart saved in: {output_path}")
