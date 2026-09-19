from textnode import *

def main():
    tn = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(tn)
    example_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    

if __name__ == "__main__":
    main()
