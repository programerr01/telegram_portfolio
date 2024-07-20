from helper import generate_json_file
def test_deployment():
    name_ = input("enter the name: ");
    title_ = input("enter the title: ");
    description_ = input("enter the description: ");
    email_ = input("enter the email: ");
    image_path_ = input("enter the image path: ");

    generate_json_file(name_, title_, description_, email_, image_path_)


if __name__ == "__main__":
    test_deployment()
