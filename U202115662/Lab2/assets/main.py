from swiftclient import Connection, ClientException
from PIL import Image
from io import BytesIO

class SwiftFileCRUD:
    def __init__(self, auth_url, user, key, container_name):
        self.auth_url = auth_url
        self.user = user
        self.key = key
        self.container_name = container_name
        self.conn = None

    def connect(self):
        try:
            self.conn = Connection(authurl=self.auth_url, user=self.user, key=self.key)
            print("Connected to Swift.")
        except ClientException as e:
            print(f"Failed to connect to Swift: {e}")

    def create_file(self, file_path, file_name):
        try:
            with open(file_path, 'rb') as file:
                file_contents = file.read()
                self.conn.put_object(self.container_name, file_name, contents=file_contents)
                print(f"File '{file_name}' created successfully in container '{self.container_name}'.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except ClientException as e:
            print(f"Failed to create file: {e}")

    def read_file(self, file_name, type):
        try:
            _, file_contents = self.conn.get_object(self.container_name, file_name)
            if type==1:
                image = Image.open(BytesIO(file_contents))
                image.show()
                print(f"File '{file_name}' retrieved and displayed successfully.")
            else:
                print(f"Contents of txt file '{file_name}': {file_contents}")
        except ClientException as e:
            print(f"Failed to read file: {e}")

    def update_file(self, file_name, new_file_path):
        try:
            with open(new_file_path, 'rb') as new_file:
                new_file_contents = new_file.read()
                self.conn.put_object(self.container_name, file_name, contents=new_file_contents)
                print(f"File '{file_name}' updated successfully.")
        except FileNotFoundError:
            print(f"New file '{new_file_path}' not found.")
        except ClientException as e:
            print(f"Failed to update file: {e}")

    def delete_file(self, file_name):
        try:
            self.conn.delete_object(self.container_name, file_name)
            print(f"File '{file_name}' deleted successfully.")
        except ClientException as e:
            print(f"Failed to delete file: {e}")

auth_url = 'http://127.0.0.1:12345/auth/v1.0'
user = 'test:tester'
key = 'testing'
container_name = 'first_try'

# 对文字文件进行 CRUD 操作
swift_text_crud = SwiftFileCRUD(auth_url, user, key, container_name)
swift_text_crud.connect()

text_file_path = './data/first.txt'  # 文字文件的路径
text_file_name = 'text_file.txt'  # 文字文件在 Swift 中的名称

# 创建并读取
swift_text_crud.create_file(text_file_path, text_file_name)
swift_text_crud.read_file(text_file_name, 0)

# 更新并读取
new_text_file_path = './data/new.txt'  # 新文字文件的路径
swift_text_crud.update_file(text_file_name, new_text_file_path)
swift_text_crud.read_file(text_file_name, 0)

# 删除，断开连接
swift_text_crud.delete_file(text_file_name)
swift_text_crud.conn.close()

# 对图片文件进行 CRUD 操作
swift_image_crud = SwiftFileCRUD(auth_url, user, key, container_name)
swift_image_crud.connect()

image_file_path = './data/first.jpg'  # 图片文件的路径
image_file_name = 'image.jpg'  # 图片文件在 Swift 中的名称

# 创建并读取
swift_image_crud.create_file(image_file_path, image_file_name)
swift_image_crud.read_file(image_file_name, 1)

# 更新并读取
new_image_file_path = './data/new.jpg'  # 新图片文件的路径
swift_image_crud.update_file(image_file_name, new_image_file_path)
swift_image_crud.read_file(image_file_name, 1)

# 删除，断开连接
swift_image_crud.delete_file(image_file_name)
swift_image_crud.conn.close()
