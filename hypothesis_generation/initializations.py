from fetcher import get_success_posts_reply_to

def load_training_data():
    post_ids = get_success_posts_reply_to("CMV.db")
    print(len(post_ids))

    return get_success_posts_reply_to("CMV.db")


if __name__ == "__main__":
    load_training_data()