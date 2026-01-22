import urllib.request
import json
import urllib.error
import random

BASE_URL = "http://127.0.0.1:8001"


def run_test():
    print(f"Testing against {BASE_URL}")

    # 1. Create User
    suffix = random.randint(10000, 99999)
    user_data = {"username": f"user{suffix}", "email": f"user{suffix}@example.com"}
    print(f"Creating user: {user_data['username']}")

    user_id = None
    req = urllib.request.Request(
        f"{BASE_URL}/api/users",
        data=json.dumps(user_data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            user = json.loads(response.read().decode())
            user_id = user["id"]
            print(f"Created user: {user_id}")
    except urllib.error.HTTPError as e:
        print(f"Error creating user: {e.code} {e.read().decode()}")
        return

    # 2. Create Post
    print("Creating post...")
    post_data = {
        "title": f"Original Title {suffix}",
        "content": "Original content.",
        "user_id": user_id,
    }
    post_id = None
    req = urllib.request.Request(
        f"{BASE_URL}/api/posts",
        data=json.dumps(post_data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            post = json.loads(response.read().decode())
            post_id = post["id"]
            print(f"Created post: {post_id}")
    except urllib.error.HTTPError as e:
        print(f"Error creating post: {e.code} {e.read().decode()}")
        return

    # 3. Update Post (PUT)
    print("Updating post (PUT)...")
    update_data = {
        "title": f"Updated Title {suffix}",
        "content": "Updated content.",
        "user_id": user_id,
    }
    # Clean update data for PostUpdate which only has title and content
    update_payload = {k: v for k, v in update_data.items() if k in ["title", "content"]}

    req = urllib.request.Request(
        f"{BASE_URL}/api/posts/{post_id}",
        data=json.dumps(update_payload).encode(),
        headers={"Content-Type": "application/json"},
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req) as response:
            updated_post = json.loads(response.read().decode())
            print(f"Updated post title: {updated_post['title']}")
            if updated_post["title"] == update_data["title"]:
                print("Update verification: SUCCESS")
            else:
                print("Update verification: FAILED (Title mismatch)")
    except urllib.error.HTTPError as e:
        print(f"Error updating post: {e.code} {e.read().decode()}")
        # Continue to patch even if put failed? Better return
        return

    # 4. Patch Post (PATCH)
    print("Patching post (PATCH)...")
    patch_data = {"title": f"Patched Title {suffix}"}
    req = urllib.request.Request(
        f"{BASE_URL}/api/posts/{post_id}",
        data=json.dumps(patch_data).encode(),
        headers={"Content-Type": "application/json"},
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req) as response:
            patched_post = json.loads(response.read().decode())
            print(f"Patched post title: {patched_post['title']}")
            # Content should remain "Updated content."
            if (
                patched_post["title"] == patch_data["title"]
                and patched_post["content"] == "Updated content."
            ):
                print("Patch verification: SUCCESS")
            else:
                print(
                    f"Patch verification: FAILED (Content: {patched_post['content']})"
                )
    except urllib.error.HTTPError as e:
        print(f"Error patching post: {e.code} {e.read().decode()}")
        return

    # 5. Delete Post (DELETE)
    print("Deleting post...")
    req = urllib.request.Request(
        f"{BASE_URL}/api/posts/{post_id}",
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Delete response code: {response.getcode()}")
            if response.getcode() == 204:
                print("Delete request: SUCCESS")
            else:
                pass
    except urllib.error.HTTPError as e:
        print(f"Error deleting post: {e.code} {e.read().decode()}")
        return

    # 6. Verify Deletion
    print("Verifying deletion...")
    try:
        urllib.request.urlopen(f"{BASE_URL}/api/posts/{post_id}")
        print("Deletion verification: FAILED (Post still exists)")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Deletion verification: SUCCESS (404 Not Found)")
        else:
            print(f"Deletion verification: FAILED (Unexpected error {e.code})")


if __name__ == "__main__":
    run_test()
