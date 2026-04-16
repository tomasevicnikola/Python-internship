import sys
import subprocess


def get_tags():
    # Get all existing git tags
    output = subprocess.check_output(
        ["git", "tag"],
        text=True
    ).strip()

    if output:
        return output.splitlines()

    return []


def get_next_version(tags):
    # Find existing RC tags
    rc_tags = []

    for tag in tags:
        if tag.startswith("rc/"):
            rc_tags.append(tag)

    # Increment version based on the latest RC tag
    if rc_tags:
        last_tag = rc_tags[-1]
        version = last_tag.split("/")[1]
        x, y, z = map(int, version.split("."))
        y += 1
    else:
        # Start from initial version if no RC tags exist
        x, y, z = 1, 0, 0

    return x, y, z


def create_git_tag(tag_name):
    # Create tag on main branch
    subprocess.run(
        ["git", "tag", tag_name, "main"],
        check=True
    )


def main():
    # Check if release tag should also be created
    create_release = "--create-release" in sys.argv

    tags = get_tags()
    x, y, z = get_next_version(tags)

    # Create RC tag
    rc_tag = f"rc/{x}.{y}.{z}"
    create_git_tag(rc_tag)

    print(f"Created RC tag: {rc_tag}")

    # Create release tag if flag is passed
    if create_release:
        release_tag = f"{x}.{y}.{z}"
        create_git_tag(release_tag)

        print(f"Created release tag: {release_tag}")


if __name__ == "__main__":
    main()