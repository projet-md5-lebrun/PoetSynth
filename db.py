"""
code à modier 
source https://www.gradio.app/guides/running-background-tasks

"""
import sqlite3
import huggingface_hub
import gradio as gr
import pandas as pd
import shutil
import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


DB_FILE = "./reviews.db"

TOKEN = os.environ.get('HUB_TOKEN')
repo = huggingface_hub.Repository(
    local_dir="data",
    repo_type="dataset",
    clone_from="freddyaboulton/gradio-reviews",
    use_auth_token=TOKEN
)
repo.git_pull()

# Set db to latest
shutil.copyfile("./data/reviews.db", DB_FILE)


# Create table if it doesn't already exist

db = sqlite3.connect(DB_FILE)
try:
    db.execute("SELECT * FROM reviews").fetchall()
    db.close()
except sqlite3.OperationalError:
    db.execute(
        '''
        CREATE TABLE reviews (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                              name TEXT, review INTEGER, comments TEXT)
        ''')
    db.commit()
    db.close()


def get_latest_reviews(db: sqlite3.Connection):
    reviews = db.execute("SELECT * FROM reviews ORDER BY id DESC limit 10").fetchall()
    total_reviews = db.execute("Select COUNT(id) from reviews").fetchone()[0]
    reviews = pd.DataFrame(reviews, columns=["id", "date_created", "name", "review", "comments"])
    return reviews, total_reviews


def add_review(name: str, review: int, comments: str):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("INSERT INTO reviews(name, review, comments) VALUES(?,?,?)", [name, review, comments])
    db.commit()
    reviews, total_reviews = get_latest_reviews(db)
    db.close()
    return reviews, total_reviews

def load_data():
    db = sqlite3.connect(DB_FILE)
    reviews, total_reviews = get_latest_reviews(db)
    db.close()
    return reviews, total_reviews


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            name = gr.Textbox(label="Name", placeholder="What is your name?")
            review = gr.Radio(label="How satisfied are you with using gradio?", choices=[1, 2, 3, 4, 5])
            comments = gr.Textbox(label="Comments", lines=10, placeholder="Do you have any feedback on gradio?")
            submit = gr.Button(value="Submit Feedback")
        with gr.Column():
            with gr.Blocks():
                gr.Markdown("Most recently created 10 rows: See full dataset [here](https://huggingface.co/datasets/freddyaboulton/gradio-reviews)")
                data = gr.Dataframe()
            count = gr.Number(label="Total number of reviews")
    submit.click(add_review, [name, review, comments], [data, count])
    demo.load(load_data, None, [data, count])


def backup_db():
    shutil.copyfile(DB_FILE, "./data/reviews.db")
    db = sqlite3.connect(DB_FILE)
    reviews = db.execute("SELECT * FROM reviews").fetchall()
    pd.DataFrame(reviews).to_csv("./data/reviews.csv", index=False)
    print("updating db")
    repo.push_to_hub(blocking=False, commit_message=f"Updating data at {datetime.datetime.now()}")


scheduler = BackgroundScheduler()
scheduler.add_job(func=backup_db, trigger="interval", seconds=60)
scheduler.start()


demo.launch()