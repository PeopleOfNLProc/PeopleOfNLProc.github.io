import sys
from datetime import date
import pandas as pd
import markdown
import random

if __name__ == "__main__":

    inx = sys.argv[1]
    input_filename = "input.xlsx"
    date_post = date.today().strftime("%Y-%m-%d")
    date_day = date.today().strftime("%B %d, %Y")

    # get data for specified index
    df = pd.read_excel(input_filename)
    instance = df.loc[int(inx)]
    first, last = instance["Name and Surname"].split()[0], " ".join(instance["Name and Surname"].split()[1:])
    output_filename = f"_posts/{date_post}-{first.lower()}-{last.lower()}.md"

    # edit template
    title = instance["Name and Surname"]
    image = f"assets/images/{first}_{last}.jpg"
    bio = instance['A tweet about yourself and your research! (280 chars)']
    twitter_id = instance['Twitter handle (e.g. @naaclhlt) (Optional)']
    explanation = instance['Explain the Lie (140 chars)']

    l = [instance['First True Fun Fact (50 chars)'], instance['Second True Fun Fact (50 chars)'], instance['A Lie Fun Fact (50 chars)']]
    random.shuffle(l)

    answer = l.index(instance['A Lie Fun Fact (50 chars)'])

    # construct tweet
    tweet_1 = f"Our new #PeopleofNLProc researcher is {first} {last} ({twitter_id}).\n\nBIO: {bio}"
    
    tweet_2 = f"Which of the next 3 facts about {first} is the lie?\n\n#1: {l[0]}\n#2: {l[1]}\n#3: {l[2]}"

    tweet_3 = f"To participate in the series, visit https://peopleofnlproc.github.io or https://forms.gle/GqdiRQFTw4LaJYmG8."

    tweet_4 = f"#{answer+1} is the correct lie.\n\n\"{explanation}\""
    
    print("TWEET #1:")
    print(tweet_1)
    print("ADD PICTURE")
    print("--------\nTWEET #2:")
    print(tweet_2)
    print("ADD POLL")
    print("--------\nTWEET #3:")
    print(tweet_3)
    print("--------\nSOLUTION TWEET:")
    print(tweet_4 + "\n")
    tweet_url = input("enter tweet url:")

    with open(output_filename, "w") as f:
        f.write(f"---\nlayout: post\ntitle: \"{title}\"\nimage: {image}\nfeatured: true\n---\n\n")
        if not pd.isnull(twitter_id):
            parsed_twitter_id = twitter_id.strip("@").lower()
            f.write(f"<a href=\"https://twitter.com/{parsed_twitter_id}\">Follow {first} on Twitter</a>\n\n")
        f.write(f"**BIO:** {bio}\n\n")
        f.write(f"Which of the next 3 facts about {first} is the lie?\n\n")
        f.write(f"1. {l[0]}\n")
        f.write(f"2. {l[1]}\n")
        f.write(f"3. {l[2]}\n\n")
        if tweet_url != "none":
            f.write(f"Join our poll on Twitter (requires Twitter account):\n\n")
            modified_tweet = tweet_2.replace("\n", "<br>")
            f.write(f"<blockquote class=\"twitter-tweet\" data-conversation=\"none\"><p lang=\"en\" dir=\"ltr\">{modified_tweet}</p>&mdash; NAACL HLT (@NAACLHLT) <a href=\"https://twitter.com/NAACLHLT/status/{tweet_url}\">{date_day}</a></blockquote> <script async src=\"https://platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>")
        f.write(f"\n\nClick below to reveal the correct lie:\n\n")
        f.write(f"<span class=\"spoiler\">#{answer+1} is the correct lie. <br><br>From {first}: \"{explanation}\"</span>.")
