import os
import shutil

'''A short script that makes a new entry automatically.'''
if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    print("Welcome to my automatic script for making empty blog posts and websites!")
    good_option = False
    while good_option is False:
        content = input("Make a [B]log or a [P]roject? ").strip()
        if content == 'B':
            prompt = 'blog'
            good_option = True
        elif content == 'P':
            prompt = 'projects'
            good_option = True
        else:
            print("Invalid option. Try again.")
    name = input(f"Enter in a name for your new item: ").strip()
    dir_name = name.replace(' ', '_')

    description = input("Enter in a short description: ").strip()
    item_path = os.path.join(current_path, 'content', prompt, dir_name)
    
    os.mkdir(item_path)
    os.mkdir(os.path.join(item_path, 'img'))

    with open(os.path.join(item_path, f'{dir_name}.html'), 'w+') as f:
        f.write("<h2>Introduction</h2>")
    
    with open(os.path.join(item_path, 'description.txt'), 'w+') as f:
        f.write(description)

    shutil.copyfile(
        os.path.join(current_path, 'img/placeholder.webp'), 
        os.path.join(item_path, f'{dir_name}.webp')
    ) 
    print("Done! Enjoy your new item!")
