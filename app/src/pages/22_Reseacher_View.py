import logging
import streamlit as st
import requests
import pandas as pd
from PIL import Image
import json
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()
style_buttons()

def delete_post(post_id):
    """Delete a post by ID"""
    try:
        response = requests.delete(f"http://host.docker.internal:4000/researcher/delete_post/{post_id}")
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Delete failed: {response.json().get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

def edit_post(post_id, current_title, current_research):
    """Edit post function"""
    try:
        response = requests.put(
            f"http://host.docker.internal:4000/researcher/update_post/{post_id}",
            json={
                "Title": current_title,
                "Research": current_research
            }
        )
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Update failed: {response.json().get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False


def display_posts(posts):
    """Display posts in Streamlit"""
    if posts:
        search_term = st.text_input("🔍 Search posts", placeholder="Search by title or content...")
    
        if search_term:
            filtered_posts = []
            for post in posts:
                title = str(post.get('Title', '')).lower()
                research = str(post.get('Research', '')).lower()
                author_name = str(post.get('ResearcherName', '')).lower()
                field_of_study = str(post.get('FieldOfStudy', '')).lower()
            
                search_lower = search_term.lower()
                if (search_lower in title or 
                    search_lower in research or 
                    search_lower in author_name or 
                    search_lower in field_of_study):
                    filtered_posts.append(post)
            posts = filtered_posts
        
            if not posts:
                st.warning(f"No posts found matching '{search_term}'")
                return
    
        st.write(f"**Showing {len(posts)} posts**")
        st.divider()

        for post in posts:
            research_post_id = post.get('ResearchPostID', 'N/A')
            title = post.get('Title', 'No Title')
            post_date = post.get('PostDate', 'No Date')
            research_content = post.get('Research', 'No Content')
            author_id = post.get('AuthorID', 'N/A')
            author_name = post.get('ResearcherName', 'Unknown Author')
            field_of_study = post.get('FieldOfStudy', 'Unknown Field')
            
            edit_key = f"edit_{research_post_id}"
            is_editing = st.session_state.get(edit_key, False)
            
            with st.expander(f"{title} ({author_name})", expanded=False):
                if is_editing:
                    # Edit mode
                    st.write("**✏️ Editing Post**")

                    with st.form(f"edit_form_{research_post_id}"):
                        new_title = st.text_input("Title", value=title, key=f"title_{research_post_id}")
                        new_research = st.text_area("Research Content", value=research_content, height=150, key=f"research_{research_post_id}")

                        col1, col2 = st.columns(2)
                        
                        with col1:
                            save_submitted = st.form_submit_button("💾 Save Changes", type="primary")
                        with col2: 
                            cancel_submitted = st.form_submit_button("❌ Cancel")

                        if save_submitted:
                            if new_title and new_research:
                                if edit_post(research_post_id, new_title, new_research):
                                    st.session_state[edit_key] = False
                                    st.rerun()
                            else:
                                st.error("❌ Please fill in both fields!")
                        
                        if cancel_submitted:
                            st.session_state[edit_key] = False
                            st.rerun()
                
                else:

                    col1, col2 = st.columns([2, 1])
                
                    with col1:
                        st.write("**Posted:**", str(post_date))
                        st.write("**Author:**", author_name)
                        st.write("**Field:**", field_of_study)
                
                    with col2:
                        st.write("**Post ID:**", research_post_id)
                
                    st.divider()
                
                    st.write("**Research Content:**")
                    st.write(research_content)
                
                    if st.session_state["AuthorID"] == author_id:
                        col1, col2 = st.columns(2)

                        with col1:
                            if st.button(f"✏️ Edit Post", key=f"edit_btn_{research_post_id}", type="secondary"):
                                st.session_state[edit_key] = True
                                st.rerun()
                    
                        with col2:
                            if st.button(f"🗑️ Delete Post", key=f"delete_{research_post_id}", type="secondary"):
                                if delete_post(research_post_id):
                                    st.success(f"Post {research_post_id} deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete post {research_post_id}")
                    else:
                        st.write("---")
    
    else:
        st.info("No posts found. Create your first post!")

def view_posts_page():
    """Main function to fetch and display posts"""
    st.title("View Research Posts")
    try:
        response = requests.get("http://host.docker.internal:4000/researcher/get_all_posts")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            
            display_posts(posts)
            
        else:
            st.error(f"Failed to load posts: {response.status_code}")
            try:
                error_data = response.json()
                st.error(f"Error: {error_data.get('error', 'Unknown error')}")
            except:
                st.error(f"Response: {response.text}")
    
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    view_posts_page()