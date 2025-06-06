import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks


# page setup
st.set_page_config(layout='wide')

# sidebar
SideBarLinks()

# load user info from session
user_id = st.session_state.get('UserID', None)
if not user_id:
    st.error("No user logged in. Please return to home page and log in.")
    st.stop()

# gets the feed by calling the feed route
def getFeed(user_id, params):
    API_URL = f"http://web-api:4000/feed/posts/{user_id}"
    try:
        response = requests.get(API_URL, params=params)
        feed = response.json()
        logger.info(f"Loaded {len(feed)} posts.")
        return feed
    except Exception as e:
        st.error(f"Error loading feed: {e}")
        st.stop()

# formats and returns the parameters necessary for getFeed
def getParams(sort, filter, search):
    params = {}
    if sort != "Newest":
        params["sort_by"] = sort.lower()
    if filter != "All":
        params["filter_by"] = filter.lower()
    if search:
        params["search"] = search
    
    return params

# update a post's upvotes, downvotes, or endorsements
# type can be either a put or delete, and metric can be either upvote, downvote, or endorsement
def updatePostUtils(type, metric, post_id, user_id):
    API_BASE = "http://web-api:4000/post_utils"
    url = f"{API_BASE}/post/{post_id}/{metric}/{user_id}"
    if type == "put":
        return requests.put(url)
    else:
        return requests.delete(url)

#page title
st.markdown(f"### {st.session_state['Roles'][0]} Feed")

#page header
header_col1, header_col2, header_col3 = st.columns([1, 1, 2])

with header_col1:
    sort = st.selectbox("Sort by…", ["Newest", "Oldest", "Top", "Bottom"])

with header_col2:
    filter = st.selectbox("Filter by…", ["All", "Following", "Saved"])

with header_col3:
    search = st.text_input("Search")

#get parameters and feed 
params = getParams(sort, filter, search)
feed = getFeed(user_id, params)

# Draw feed
for post in feed:
    # Outer card
    with st.container():
        c1, c2, c3 = st.columns([0.1, 0.6, 0.3], vertical_alignment="center")

        with c1:
                # Upvotes, Downvotes, Endorsements
                with st.container():
                    if (post["upvoted"]) == "Upvoted":
                        upvoteIcon = "⬆"
                    else:
                        upvoteIcon = "⇧"
                    if (post["downvoted"]) == "Downvoted":
                        downvoteIcon = "⬇"
                    else:
                        downvoteIcon = "⇩"
                    if (post["endorsed"]) == "Endorsed":
                        endorsedIcon = "✅"
                    else:
                        endorsedIcon = "✔️"
                    
                    if st.button(label=upvoteIcon, key=f'upvote{post["PostID"]}'):
                        if post['upvoted'] == "Upvoted":
                            response = updatePostUtils("delete", "upvote", post["PostID"], user_id)
                        else:
                            response = updatePostUtils("put", "upvote", post["PostID"], user_id)

                        if response.status_code == 200:
                            st.rerun()
                    st.html(f"<p style='font-size: 30px; text-align: right; margin-right: 60px'>{str(post['karma'])}</p>")
                    if st.button(label=downvoteIcon, key=f'downvote{post["PostID"]}'):
                        if post['downvoted'] == "Downvoted":
                            response = updatePostUtils("delete", "downvote", post["PostID"], user_id)
                        else:
                            response = updatePostUtils("put", "downvote", post["PostID"], user_id)

                        if response.status_code == 200:
                            st.rerun()
                with st.container():
                    c1a, c1b = st.columns([0.8, 0.2], vertical_alignment="bottom")

                    with c1a:
                        if st.button(label=endorsedIcon, key=f'endorsement{post["PostID"]}', type='secondary'):
                            if post['endorsed'] == "Endorsed":
                                response = updatePostUtils("delete", "endorsement", post["PostID"], user_id)
                            else:
                                response = updatePostUtils("put", "endorsement", post["PostID"], user_id)

                            if response.status_code == 200:
                                st.rerun()

                    with c1b:
                        st.html(f"<p style='font-size: 15px; text-align: left; margin-left: -30px; margin-bottom: -10px'>{str(post['NumEndorsements'])}</p>")

        with c2:
            # Title, Author, Description
            st.markdown(f"### {post['Title']}")
            st.markdown(f"**{post['author']}**")
            st.markdown(post['Description'])

            # Show more
            st.markdown("**Show more**")

        with c3:
            # Bookmark button (simple placeholder)
            if post['bookmarked'] == 'Saved':
                bookmark_icon = "💾"
            else:
                bookmark_icon = "Not Saved"

            if st.button(f"{bookmark_icon}", key=f"bookmark_{post['PostID']}"):
                if post['bookmarked'] == "Saved":
                    response = updatePostUtils("delete", "bookmark", post["PostID"], user_id)
                else:
                    response = updatePostUtils("put", "bookmark", post["PostID"], user_id)

                if response.status_code == 200:
                    st.rerun()

            # Graph (placeholder image — replace with your GraphID renderer)
            st.image("assets/posts/placeholderGraph.gif")

    # Divider between posts
    st.markdown("---")
