import socket 
# import โมดูล socket ใช้สำหรับการสร้างและจัดการการเชื่อมต่อทางเครือข่ายโดยใช้โปรโตคอล TCP/IP ทำให้สามารถสร้าง socket server และ client เพื่อรับส่งข้อมูลระหว่างเครื่องคอมพิวเตอร์ได้
import threading
# import โมดูล threading ใช้สำหรับการทำงานแบบหลายเธรด (multithreading) ซึ่งทำให้สามารถดำเนินการหลายอย่างพร้อมกันในโปรแกรมเดียวกันได้ ตัวอย่างเช่น การรับการเชื่อมต่อใหม่จากเพื่อนร่วมเครือข่ายในขณะที่ยังสามารถประมวลผลข้อมูลจากเพื่อนร่วมเครือข่ายที่เชื่อมต่ออยู่ได้
import json
# import โมดูล json ใช้สำหรับการเข้ารหัสและถอดรหัสข้อมูลในรูปแบบ JSON (JavaScript Object Notation) ซึ่งเป็นรูปแบบที่นิยมใช้ในการแลกเปลี่ยนข้อมูลระหว่างเครื่องคอมพิวเตอร์ เนื่องจากมีโครงสร้างที่อ่านง่ายและสามารถใช้ได้ในหลายภาษาโปรแกรมมิ่ง

import sys
# import โมดูล sys ใช้สำหรับการจัดการกับตัวแปรและฟังก์ชันของระบบ เช่น การรับค่าจาก command line arguments (ตัวอย่างเช่น port ที่ใช้ในการเชื่อมต่อ)

import os
# import โมดูล os ใช้สำหรับการจัดการกับระบบไฟล์และโฟลเดอร์ เช่น การตรวจสอบว่ามีไฟล์อยู่หรือไม่ การสร้างหรือการลบไฟล์และโฟลเดอร์ เป็นต้น
import secrets
# import โมดูล secrets ใช้สำหรับการสร้างข้อมูลสุ่มที่ปลอดภัยในเชิงคริปโตกราฟี (cryptographically secure) เช่น การสร้างรหัสผ่านที่ปลอดภัย การสร้าง token ฯลฯ ในโปรแกรมนี้ใช้ secrets สำหรับการสร้างที่อยู่กระเป๋าเงิน (wallet address) ที่มีความเป็นเอกลักษณ์

class Node:
    def __init__(self, host, port):
        # เป็นตัวกำหนดค่าพื้นฐานของโหนด เช่น host, port, รายการ peers ที่เชื่อมต่อ, socket, รายการ transactions, ไฟล์สำหรับบันทึก transactions, และสร้าง wallet address สำหรับโหนดนี้
        self.host = host
        # กำหนดค่า host ให้กับตัวแปรอินสแตนซ์ self.host
        self.port = port
        # กำหนดค่า port ให้กับตัวแปรอินสแตนซ์ self.port 
        # คำสั่ง self.host = host และ self.port = port เป็นการกำหนดค่าพารามิเตอร์ให้กับวัตถุ (object) ของคลาส Node โดยเฉพาะ
        self.peers = []  # เก็บรายการ socket ของ peer ที่เชื่อมต่อ
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #  สร้างซ็อกเก็ต TCP ที่ใช้โปรโตคอล IPv4
        # เพื่อสร้างช่องทางการสื่อสารผ่านเครือข่าย โดยใช้โปรโตคอล TCP และ IPv4 ซึ่งทำให้สามารถเชื่อมต่อและสื่อสารข้อมูลระหว่างโหนดต่างๆ ในเครือข่ายเพียร์ทูเพียร์ได้   
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # กำหนดค่าซ็อกเก็ตให้สามารถใช้พอร์ตเดียวกันได้ทันทีหลังจากที่มันถูกปิด
        # ตัวแปรอื่นๆ และการตั้งค่าอื่นๆ ในคลาส
        # เพื่อปรับแต่งการทำงานของซ็อกเก็ต ให้สามารถใช้งานพอร์ตเดิมได้ทันทีหลังจากที่ซ็อกเก็ตถูกปิด ซึ่งมีประโยชน์ในกรณีที่ต้องการรีสตาร์ทโหนดใหม่อย่างรวดเร็ว โดยไม่ต้องรอให้พอร์ตถูกปล่อยออกจากสถานะ TIME_WAIT
        self.transactions = []  # เก็บรายการ transactions
        self.transaction_file = f"transactions_{port}.json"  # ไฟล์สำหรับบันทึก transactions
        self.wallet_address = self.generate_wallet_address()  # สร้าง wallet address สำหรับโหนดนี้

    def generate_wallet_address(self):
        #สร้างที่อยู่กระเป๋าเงิน (wallet address) แบบง่ายๆ โดยใช้ secrets.token_hex(20) 
        return '0x' + secrets.token_hex(20)
        #ใช้ในการสร้างและคืนค่าที่อยู่กระเป๋าเงิน (wallet address) แบบสุ่มในรูปแบบที่นิยมใช้ในระบบคริปโตเคอเรนซี (cryptocurrency) โดยมีการนำหน้าด้วย '0x' ซึ่งเป็นมาตรฐานของที่อยู่ในระบบ Ethereum และอื่นๆ
    def start(self):
        #  เริ่มต้นการทำงานของโหนด โดยทำการ bind socket กับ host และ port ที่ระบุ, เริ่มฟังการเชื่อมต่อใหม่, โหลด transactions จากไฟล์ และเริ่ม thread สำหรับรับการเชื่อมต่อใหม่
        self.socket.bind((self.host, self.port))
        # ผูกซ็อกเก็ตกับที่อยู่ IP และพอร์ต
        self.socket.listen(1)
        # เริ่มฟังการเชื่อมต่อใหม่
        print(f"Node listening on {self.host}:{self.port}")
        # แสดงข้อความว่ากำลังrunที่ IP และพอร์ตใด
        print(f"Your wallet address is: {self.wallet_address}")
        #   แสดงที่อยู่กระเป๋าเงินของโหนด 
        self.load_transactions()  # โหลด transactions จากไฟล์ (ถ้ามี)

        # เริ่ม thread สำหรับรับการเชื่อมต่อใหม่
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()
        # คำสั่ง accept_thread = threading.Thread(target=self.accept_connections) และ accept_thread.start() ใช้เพื่อสร้างและเริ่มต้นการทำงานของเธรดใหม่ที่ทำหน้าที่รับการเชื่อมต่อใหม่จากเพียร์ (peer) อื่นๆ ในเครือข่าย
        # threading.Thread() เป็นฟังก์ชันที่ใช้เพื่อสร้างเธรดใหม่

        # target=self.accept_connections กำหนดฟังก์ชันที่เธรดนี้จะรัน เมื่อเธรดถูกเริ่มต้น ซึ่งในกรณีนี้คือฟังก์ชัน self.accept_connections

        # ฟังก์ชัน accept_connections จะถูกเรียกใช้ในเธรดใหม่นี้ ซึ่งช่วยให้โหนดสามารถรับการเชื่อมต่อใหม่ได้อย่างต่อเนื่อง โดยไม่บล็อกการทำงานหลักของโปรแกรม

        # start() เป็นฟังก์ชันที่ใช้เพื่อเริ่มต้นการทำงานของเธรดที่ถูกสร้างขึ้น

        # เมื่อเรียกใช้ accept_thread.start() เธรดจะเริ่มทำงานและรันฟังก์ชัน self.accept_connections ในเธรดนั้น

    def accept_connections(self):
        # รอรับการเชื่อมต่อใหม่จากเพื่อนร่วมเครือข่าย เมื่อมีการเชื่อมต่อใหม่เข้ามา จะสร้าง thread ใหม่สำหรับจัดการการเชื่อมต่อนั้น
        while True:
            # รอรับการเชื่อมต่อใหม่
            client_socket, address = self.socket.accept()
            # client_socket, address = self.socket.accept() ใช้เพื่อรับการเชื่อมต่อใหม่จากผู้เชื่อมต่อ (client) ซึ่งเรียกว่าการยอมรับการเชื่อมต่อ (accepting connections) โดยใช้ฟังก์ชัน accept() ของซ็อกเก็ตที่ถูกผูกไว้กับโหนดนี้
            # เมื่อมีการเรียกใช้ accept() จะเกิดการบล็อก (block) โดยโปรแกรมจะรอรับการเชื่อมต่อจาก client ใหม่ ซึ่งจะส่งคืน client_socket ซึ่งเป็นซ็อกเก็ตใหม่ที่ใช้ในการสื่อสารกับ client ที่เชื่อมต่อเข้ามา และ address ที่เก็บที่อยู่ IP และพอร์ตของ client ที่เชื่อมต่อเข้ามาใหม่
            print(f"New connection from {address}")
            # แสดง ข้อความ New connection form ตามด้วยที่อยู่ address ที่ส่งมา


            # เริ่ม thread ใหม่สำหรับจัดการการเชื่อมต่อนี้
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            # client_thread = threading.Thread(target=self.handle_client, args=(client_socket,)) และ client_thread.start() ใช้สร้างเธรดใหม่เพื่อจัดการการสื่อสารกับ client ที่เชื่อมต่อเข้ามาใหม่ โดยใช้ฟังก์ชัน handle_client เพื่อดำเนินการรับส่งข้อมูลกับ client นั้น ๆ
            # threading.Thread() เป็นฟังก์ชันที่ใช้สร้างเธรดใหม่
            # target=self.handle_client กำหนดให้เธรดใหม่รันฟังก์ชัน self.handle_client
            # args=(client_socket,) คือพารามิเตอร์ที่จะส่งให้กับฟังก์ชัน handle_client ซึ่งในที่นี้คือ 
            #client_socket ที่เป็นซ็อกเก็ตสำหรับการสื่อสารกับ client นั้น 
            client_thread.start()
            # start() เป็นเมธอดที่ใช้เริ่มต้นการทำงานของเธรดใหม่ที่ถูกสร้างขึ้น
            # เมื่อเรียกใช้ start() เธรดจะเริ่มทำงานและรันฟังก์ชัน self.handle_client ในเธรดนั้น ๆ 

    def handle_client(self, client_socket):
        # จัดการกับการเชื่อมต่อจากเพื่อนร่วมเครือข่าย โดยรับข้อมูลจาก client และประมวลผลข้อมูลนั้น
        while True:
            # เป็นลูปที่วิ่งไปเรื่อยๆ เพื่อรอรับข้อมูลจาก client และประมวลผลตามต่อมา
            try:
                # ในบล็อก try จะทำการรับข้อมูลจาก client โดยใช้ client_socket.recv(1024) ซึ่งรับข้อมูลจาก client ได้ไม่เกิน 1024 bytes ในการรับครั้งหนึ่ง
                # รับข้อมูลจาก client
                data = client_socket.recv(1024)
                if not data:
                    break
                    #  # หากไม่มีข้อมูลที่รับมา (if not data:) แสดงว่า client ได้ปิดการเชื่อมต่อ ดังนั้นจะออกจากลูปด้วย break
                message = json.loads(data.decode('utf-8'))
                # message = json.loads(data.decode('utf-8')):
                # แปลงข้อมูลที่รับมาจาก client (ซึ่งเป็นข้อมูลในรูปแบบ bytes) ให้เป็นข้อมูล JSON โดยใช้ json.loads() และ data.decode('utf-8') เพื่อแปลงเป็นข้อความในรูปแบบ Unicode
                
                self.process_message(message, client_socket)
                # เรียกใช้เมท็อด process_message ของคลาส Node เพื่อประมวลผลข้อความที่ได้รับจาก client


            except Exception as e:
                # ถ้าเกิดข้อผิดพลาดในการรับหรือประมวลผลข้อมูลจาก client จะเข้าสู่บล็อก except เพื่อจัดการข้อผิดพลาดนั้น
                print(f"Error handling client: {e}")
                break
                # ในที่นี้จะแสดงข้อผิดพลาดที่เกิดขึ้นในการประมวลผลด้วย print(f"Error handling client: {e}") และจะออกจากลูปด้วย break

        client_socket.close()
        # เมื่อลูป while True จบลง (เช่น เมื่อ client ปิดการเชื่อมต่อ) จะปิดซ็อกเก็ต (socket) ด้วย client_socket.close() เพื่อปิดการเชื่อมต่อกับ client นั้น

    def connect_to_peer(self, peer_host, peer_port):
        # สร้างการเชื่อมต่อไปยังเพื่อนร่วมเครือข่ายที่ระบุ และขอข้อมูล transactions ทั้งหมดจาก peer ที่เชื่อมต่อ
        try:
            # สร้างการเชื่อมต่อไปยัง peer
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # สร้างซ็อกเก็ตใหม่สำหรับการเชื่อมต่อกับ peer โดยใช้โปรโตคอล TCP/IP (SOCK_STREAM)
            # AF_INET ระบุว่าจะใช้ IPv4 สำหรับการเชื่อมต่อ
            peer_socket.connect((peer_host, peer_port))
            # เชื่อมต่อไปยัง peer ที่กำหนดด้วย peer_host (ที่อยู่ IP หรือ DNS) และ peer_port (หมายเลขพอร์ต)
            
            self.peers.append(peer_socket)
            # เมื่อการเชื่อมต่อสำเร็จแล้วจะสร้างการเชื่อมต่อที่เก็บไว้ใน self.peers และแสดงข้อความว่าเชื่อมต่อสำเร็จ
            print(f"Connected to peer {peer_host}:{peer_port}")

            # ขอข้อมูล transactions ทั้งหมดจาก peer ที่เชื่อมต่อ
            self.request_sync(peer_socket)
            # เรียกใช้เมท็อด request_sync เพื่อขอข้อมูลการซิงโครไนซ์จาก peer ที่เชื่อมต่อเข้ามา

            # เริ่ม thread สำหรับรับข้อมูลจาก peer นี้
            peer_thread = threading.Thread(target=self.handle_client, args=(peer_socket,))
            # สร้างเธรดใหม่ (peer_thread) เพื่อรับข้อมูลจาก peer นี้โดยใช้ฟังก์ชัน handle_client ซึ่งรับ peer_socket เป็นพารามิเตอร์

            peer_thread.start()
            # เริ่มเธรดใหม่เพื่อรับข้อมูลจาก peer นี้

        except Exception as e:
            # ถ้าเกิดข้อผิดพลาดในขั้นตอนใดของการเชื่อมต่อ (เช่น ไม่สามารถเชื่อมต่อไปยัง peer ได้) จะเข้าสู่บล็อก except และแสดงข้อความว่าเกิดข้อผิดพลาดที่เกิดขึ้น
            print(f"Error connecting to peer: {e}")

    def broadcast(self, message):
        # ฟังก์ชัน broadcast ใช้สำหรับส่งข้อมูล (message) ไปยังทุก peer ที่เชื่อมต่ออยู่กับโหนดนี้ในเครือข่าย โดยใช้การส่งข้อมูลผ่านซ็อกเก็ตของแต่ละ peer ใน self.peers ซึ่งเก็บรายการของซ็อกเก็ตที่เชื่อมต่อไปยังแต่ละ peer.
        # ส่งข้อมูลไปยังทุก peer ที่เชื่อมต่ออยู่
        for peer_socket in self.peers:
            # ลูปผ่านทุก peer ที่เชื่อมต่ออยู่กับโหนดนี้ ซึ่งเก็บไว้ใน self.peers
            try:
                peer_socket.send(json.dumps(message).encode('utf-8'))
                # ส่งข้อมูล message ไปยัง peer โดยใช้ send() ของซ็อกเก็ต peer_socket
                # json.dumps(message) ใช้เปลี่ยนข้อมูล message ให้เป็นรูปแบบ JSON string
                # encode('utf-8') ใช้แปลงข้อมูล JSON string เป็น byte object ที่ใช้ในการส่งผ่านซ็อกเก็ต
            except Exception as e:
                # ถ้าเกิดข้อผิดพลาดในขณะที่ส่งข้อมูล (เช่น peer ปิดการเชื่อมต่ออยู่) จะเข้าสู่บล็อก except และแสดงข้อความเกี่ยวกับข้อผิดพลาดที่เกิดขึ้น
                print(f"Error broadcasting to peer: {e}")

                self.peers.remove(peer_socket)
                # หากเกิดข้อผิดพลาดในการส่งข้อมูล โค้ดนี้จะพยายามลบ peer_socket ออกจาก self.peers เพื่อไม่ต้องส่งข้อมูลไปยัง peer ที่ไม่สามารถเชื่อมต่อได้ต่อไป

    def process_message(self, message, client_socket):
    # ฟังก์ชัน process_message ใช้สำหรับประมวลผลข้อความที่รับเข้ามาผ่าน client_socket จาก peer หรือ client ที่เชื่อมต่อเข้ามากับโหนดนี้ในเครือข่าย โดยจะดำเนินการตามประเภทของข้อความที่รับมาในรูปแบบ JSON ซึ่งมักจะใช้ในการสื่อสารระหว่างโหนดซึ่งเป็นส่วนหนึ่งของบล็อกเชนหรือระบบที่ใช้เทคโนโลยี Blockchain ได้แก่การเพิ่ม transaction ใหม่ การขอซิงโครไนซ์ข้อมูล หรือการตอบกลับของการซิงโครไนซ์ข้อมูลที่ขอไปจาก peer อื่น ๆ ในเครือข่าย 
        # ประมวลผลข้อความที่ได้รับ เช่น การเพิ่ม transaction ใหม่ การซิงโครไนซ์ข้อมูล ฯลฯ
        if message['type'] == 'transaction':
            # กรณีที่ประเภทของข้อความ (message['type']) เป็น 'transaction'
            # แสดงข้อความที่รับได้ว่าได้รับ transaction และแสดงข้อมูล transaction ที่ได้รับ
            print(f"Received transaction: {message['data']}")
            self.add_transaction(message['data'])
            # เรียกใช้เมท็อด add_transaction เพื่อเพิ่ม transaction ลงในโหนดนี้
        elif message['type'] == 'sync_request': 
            # กรณีที่ประเภทของข้อความ (message['type']) เป็น 'sync_request'
            self.send_all_transactions(client_socket)
            # เรียกใช้เมท็อด send_all_transactions เพื่อส่งข้อมูล transactions ทั้งหมดไปยัง peer ที่ขอซิงโครไนซ์ (ผ่าน client_socket)
        elif message['type'] == 'sync_response':
            # กรณีที่ประเภทของข้อความ (message['type']) เป็น 'sync_response'
            self.receive_sync_data(message['data'])
            # เรียกใช้เมท็อด receive_sync_data เพื่อรับและประมวลผลข้อมูลการซิงโครไนซ์ที่ได้รับมาจาก peer
        else:
            print(f"Received message: {message}")
            # กรณีที่ประเภทของข้อความไม่ตรงกับที่ระบุไว้ (ไม่ใช่ 'transaction', 'sync_request', หรือ 'sync_response')
            # แสดงข้อความว่าได้รับข้อความที่ไม่รู้จักประเภท

    def add_transaction(self, transaction):
        # ฟังก์ชัน add_transaction ใช้สำหรับเพิ่ม transaction ใหม่ลงในโหนดและทำการบันทึกลงในไฟล์เพื่อให้สามารถเก็บข้อมูล transactions ไว้ตลอดเวลา
        # เพิ่ม transaction ใหม่และบันทึกลงไฟล์
        if transaction not in self.transactions:
            # ตรวจสอบว่า transaction ที่รับเข้ามายังไม่มีอยู่ใน self.transactions หรือไม่
            self.transactions.append(transaction)
            # หาก transaction ยังไม่มีอยู่ใน self.transactions จะทำการเพิ่ม transaction นี้เข้าไปในลิสต์ self.transactions
            self.save_transactions()
            # เรียกใช้เมท็อด save_transactions เพื่อบันทึก transactions ล่าสุดลงในไฟล์
            print(f"Transaction added and saved: {transaction}")
            # แสดงข้อความบอกว่า transaction ได้ถูกเพิ่มและบันทึกลงในไฟล์เรียบร้อย

    def create_transaction(self, recipient, amount):
        # ฟังก์ชัน create_transaction ใช้สำหรับสร้าง transaction ใหม่และส่งข้อมูล transaction ไปยังทุก peer ที่เชื่อมต่ออยู่กับโหนดนี้ในเครือข่าย 
        # สร้าง transaction ใหม่และส่งข้อมูลไปยังทุก peer ที่เชื่อมต่ออยู่
        transaction = {
            # สร้าง dictionary transaction ที่ประกอบด้วยข้อมูล sender (wallet address ของโหนด), recipient (wallet address ของผู้รับ), และ amount (จำนวนเงินที่จะส่ง)
            'sender': self.wallet_address,
            'recipient': recipient,
            'amount': amount
        }
        self.add_transaction(transaction)
        # เรียกใช้เมท็อด add_transaction เพื่อเพิ่ม transaction ลงในโหนดของตนเอง
        self.broadcast({'type': 'transaction', 'data': transaction})
        # เรียกใช้เมท็อด broadcast เพื่อส่งข้อมูล transaction ไปยังทุก peer ที่เชื่อมต่ออยู่
        # ข้อมูลที่ส่งไปจะเป็น JSON object ที่มี type เป็น 'transaction' และ data เป็นข้อมูล transaction ที่สร้างขึ้น

    def save_transactions(self):
        # ฟังก์ชัน save_transactions ใช้สำหรับบันทึกข้อมูล transactions ลงในไฟล์ JSON ที่เก็บไว้ในโหนดนี้ 
        # บันทึก transactions ลงไฟล์
        with open(self.transaction_file, 'w') as f:
            # เปิดไฟล์ self.transaction_file ในโหมดเขียน ('w') โดยใช้คำสั่ง open() ซึ่งจะทำการสร้างไฟล์ใหม่หากยังไม่มีไฟล์นี้อยู่

            json.dump(self.transactions, f)
            # ใช้ json.dump() เพื่อเขียนข้อมูลจาก self.transactions (ซึ่งเป็นลิสต์ของ transactions) ลงในไฟล์ที่เปิดไว้ในขั้นตอนที่ 1
            # ใช้ with statement เพื่อให้ Python ทำการปิดไฟล์โดยอัตโนมัติหลังจากที่เสร็จสิ้นการเขียน


    def load_transactions(self):
        # ฟังก์ชัน load_transactions ใช้สำหรับโหลดข้อมูล transactions จากไฟล์ JSON ที่เก็บไว้ในโหนดนี้
        # โหลด transactions จากไฟล์ (ถ้ามี)
        if os.path.exists(self.transaction_file):
            # ใช้ os.path.exists(self.transaction_file) เพื่อตรวจสอบว่าไฟล์ self.transaction_file ที่เก็บ transactions อยู่แล้วหรือยัง
            with open(self.transaction_file, 'r') as f:
                # ถ้ามีไฟล์อยู่ (if os.path.exists(self.transaction_file) เป็น True) จะใช้ open(self.transaction_file, 'r') เพื่อเปิดไฟล์ในโหมดอ่าน ('r')
                self.transactions = json.load(f)
                # ใช้ json.load(f) เพื่อโหลดข้อมูลจากไฟล์ที่เปิดไว้ในตัวแปร f (ซึ่งเป็น file object) และเก็บไว้ใน self.transactions
            print(f"Loaded {len(self.transactions)} transactions from file.")
            # แสดงข้อความที่บอกว่าได้โหลด transactions จากไฟล์เรียบร้อยแล้ว พร้อมกับจำนวน transactions ทั้งหมดที่โหลดเข้ามา


    def request_sync(self, peer_socket):
        # ฟังก์ชัน request_sync ใช้สำหรับส่งคำขอซิงโครไนซ์ข้อมูล transactions ไปยังโหนด peer ที่เชื่อมต่ออยู่ผ่าน peer_socket ที่รับเข้ามาเป็นพารามิเตอร์ 
        # ส่งคำขอซิงโครไนซ์ไปยัง peer
        sync_request = json.dumps({"type": "sync_request"}).encode('utf-8')
        # ใช้ json.dumps({"type": "sync_request"}) เพื่อแปลง dictionary {"type": "sync_request"} เป็น JSON string
        #  ใช้ .encode('utf-8') เพื่อแปลง JSON string เป็น byte string ในรูปแบบ UTF-8 ซึ่งเป็นรูปแบบที่ socket ใช้ในการส่งข้อมูล
        peer_socket.send(sync_request)
        # ใช้ peer_socket.send(sync_request) เพื่อส่ง byte string ที่เป็นข้อความ sync_request ไปยังโหนด peer ที่เชื่อมต่ออยู่ผ่าน socket

    def send_all_transactions(self, client_socket):
        # ฟังก์ชัน send_all_transactions ใช้สำหรับส่งข้อมูล transactions ทั้งหมดไปยังโหนดที่ขอซิงโครไนซ์ (sync) ผ่าน client_socket ที่รับเข้ามาเป็นพารามิเตอร์
        # ส่ง transactions ทั้งหมดไปยังโหนดที่ขอซิงโครไนซ์
        sync_data = json.dumps({
            # ใช้ json.dumps() เพื่อแปลง dictionary ที่มีโครงสร้าง {"type": "sync_response", "data": self.transactions} เป็น JSON string
            "type": "sync_response",
            "data": self.transactions
        }).encode('utf-8')
        # จากนั้นใช้ .encode('utf-8') เพื่อแปลง JSON string เป็น byte string ในรูปแบบ UTF-8 ซึ่งเป็นรูปแบบที่ socket ใช้ในการส่งข้อมูล
        client_socket.send(sync_data)
        # ช้ client_socket.send(sync_data) เพื่อส่ง byte string ที่เป็นข้อมูล sync_data ไปยังโหนดที่ขอซิงโครไนซ์ผ่าน socket ที่รับมาในฟังก์ชัน
    def receive_sync_data(self, sync_transactions):
        # ฟังก์ชัน receive_sync_data ใช้สำหรับรับและประมวลผลข้อมูล transactions ที่ได้รับจากการซิงโครไนซ์จากโหนดอื่นในเครือข่าย 
        # รับและประมวลผลข้อมูล transactions ที่ได้รับจากการซิงโครไนซ์
        for tx in sync_transactions:
            # ใช้ for tx in sync_transactions: เพื่อวนลูปผ่านข้อมูลทุกตัวใน sync_transactions ซึ่งมีโครงสร้างเป็นลิสต์ของ transactions ที่ถูกส่งมาจากโหนดอื่น
            self.add_transaction(tx)
            # สำหรับแต่ละ transaction (tx) ที่ได้รับมา ใช้ self.add_transaction(tx) เพื่อเพิ่ม transaction เข้าไปใน self.transactions ของโหนดปัจจุบัน
            # add_transaction จะทำการเพิ่ม transaction ใหม่เข้าไปในลิสต์ self.transactions และทำการบันทึกข้อมูลลงในไฟล์ที่เก็บ transactions ของโหนด

        print(f"Synchronized {len(sync_transactions)} transactions.")
        # พิมพ์ข้อความที่บอกว่ามี transactions จำนวนเท่าไรที่ถูกซิงโครไนซ์เข้ามาเรียบร้อยแล้ว โดยใช้ print(f"Synchronized {len(sync_transactions)} transactions.")

if __name__ == "__main__":
    # เมื่อโค้ดถูกนำเข้าและใช้งานโดยโมดูลอื่น โค้ดที่อยู่ภายใน if __name__ == "__main__": จะไม่ถูกเรียกใช้ แต่จะเป็นไปตามลำดับของการเรียกใช้ฟังก์ชันหรือคลาสที่มีอยู่ในโมดูลนั้น ๆ
    # print("Exiting...")
    if len(sys.argv) != 2:
        print("Usage: python script.py <port>")
        sys.exit(1)
        # ตรวจสอบว่าผู้ใช้ได้ระบุพอร์ต (port) ผ่าน command line argument ในการรันโปรแกรมหรือไม่ ถ้าผู้ใช้ไม่ได้ใส่พอร์ตหรือใส่ผิดรูปแบบ โปรแกรมจะแสดงข้อความ "Usage: python script.py <port>" เพื่อแสดงวิธีการใช้งานที่ถูกต้อง และจากนั้นโปรแกรมจะจบการทำงานด้วย sys.exit(1) เพื่อออกจากโปรแกรมโดยมีการส่งโค้ดออกแสดงความผิดพลาดด้วยค่า 1 (ที่แสดงถึงข้อผิดพลาดที่ไม่ได้ระบุพอร์ตอย่างถูกต้อง).
        # หลังจากนั้นโปรแกรมจะสร้างวัตถุ Node ด้วย IP address "0.0.0.0" ซึ่งหมายถึงให้โหนดนี้รับการเชื่อมต่อจากภายนอกได้ทุกที่ และพอร์ตที่ผู้ใช้ระบุผ่าน command line argument จากนั้นโปรแกรมจะเริ่มต้นการทำงานของโหนดด้วยเมทอด node.start() ซึ่งทำหน้าที่เชื่อมต่อและเริ่มการทำงานของโหนดในเครือข่ายหรือทำงานตามที่โปรแกรมโน้ดกำหนดไว้ในตัวอย่างโค้ดที่ได้แสดงไว้ข้างต้น.
    
    port = int(sys.argv[1])
    node = Node("0.0.0.0", port)  # ใช้ "0.0.0.0" เพื่อรับการเชื่อมต่อจากภายนอก
    node.start()
    # การรับพารามิเตอร์ผ่าน command line
    # โปรแกรมรับพารามิเตอร์ port ผ่าน command line โดยใช้ sys.argv ซึ่งในที่นี้ต้องรับพารามิเตอร์เพียง 1 ตัวคือ <port>
    # ถ้าจำนวนพารามิเตอร์ไม่เท่ากับ 2 (รวมชื่อของ script ด้วย) โปรแกรมจะแสดงข้อความ "Usage: python script.py <port>" และจบการทำงานด้วย sys.exit(1) เพื่อออกจากโปรแกรม
    
    while True:
        # loop จะทำงานตลอด
        print("\n1. Connect to a peer")
        # แสดงข้อความ 1.Connect to a peer
        print("2. Create a transaction")
        # แสดงข้อความ 2. Create a transaction
        print("3. View all transactions")
        # แสดงข้อความ 3. View all transactions
        print("4. View my wallet address")
        # แสดงข้อความ 4. View my wallet address 
        print("5. Exit")
        # แสดงข้อความ 5. Exit
        choice = input("Enter your choice: ")
        # คำสั่ง input("Enter your choice: ") ใน Python ใช้ในการรับข้อมูลจากผู้ใช้ผ่านคีย์บอร์ด โดยจะแสดงข้อความ "Enter your choice: " บนหน้าจอเพื่อให้ผู้ใช้ระบุข้อมูลที่ต้องการให้โปรแกรมดำเนินการต่อ ในกรณีนี้คือการเลือกตัวเลือกจากเมนูที่แสดง ตัวอย่างเช่น ผู้ใช้จะพิมพ์ '1' เพื่อเชื่อมต่อกับโหนดพีร์ หรือ '2' เพื่อสร้างธุรกรรมใหม่ แล้วกด Enter สำหรับโปรแกรมจะดำเนินการตามเงื่อนไขที่กำหนดไว้ในโค้ดที่ต่อจากนั้น
        
        if choice == '1':
            # โค้ดที่แสดงนี้เป็นการตรวจสอบค่าของตัวแปร choice ซึ่งได้รับค่าจากผู้ใช้ผ่านการรับข้อมูลจากคีย์บอร์ด (ด้วย input()). การทำงานของโค้ดจะดำเนินการตามตัวเลือกที่ผู้ใช้เลือก:
            # เลือก '1': ผู้ใช้จะถูกให้ป้อน host และ port ของโหนดที่ต้องการเชื่อมต่อเข้ากับโหนดปลายทางผ่าน input() จากนั้นโปรแกรมจะเรียกใช้เมทอด node.connect_to_peer(peer_host, peer_port) เพื่อเชื่อมต่อกับโหนดนั้น.
            peer_host = input("Enter peer host to connect: ")
            peer_port = int(input("Enter peer port to connect: "))
            node.connect_to_peer(peer_host, peer_port)
        elif choice == '2':
            recipient = input("Enter recipient wallet address: ")
            amount = float(input("Enter amount: "))
            node.create_transaction(recipient, amount)
            # เลือก '2': ผู้ใช้จะถูกให้ป้อนที่อยู่วอลเล็ตของผู้รับและจำนวนเงินที่ต้องการส่ง จากนั้นโปรแกรมจะสร้างธุรกรรมใหม่ด้วยเมทอด node.create_transaction(recipient, amount) และส่งข้อมูลธุรกรรมนี้ไปยังโหนดอื่นในเครือข่าย.
        elif choice == '3':
            print("All transactions:")
            for tx in node.transactions:
                print(tx)
                # เลือก '3': โปรแกรมจะแสดงรายการธุรกรรมทั้งหมดที่โหนดนี้เคยบันทึกไว้ โดยการใช้ลูป for เพื่อพิมพ์ทุกรายการธุรกรรมจาก node.transactions.
        elif choice == '4':
            print(f"Your wallet address is: {node.wallet_address}")
            # เลือก '4': โปรแกรมจะแสดงที่อยู่วอลเล็ตของโหนดนี้ ซึ่งถูกเก็บไว้ใน node.wallet_address.
        elif choice == '5':
            # เลือก '5': ถ้าผู้ใช้เลือกเลข 5 โปรแกรมจะออกจากการทำงานด้วยคำสั่ง break ซึ่งทำให้ลูป while ที่ครอบโค้ดนี้จบการทำงานและโปรแกรมจะปิดตัวลง.
            break
        else:
            print("Invalid choice. Please try again.")

            # ถ้าผู้ใช้ป้อนเลือกที่ไม่ถูกต้อง: โปรแกรมจะพิมพ์ข้อความ "Invalid choice. Please try again." และให้ผู้ใช้ทำการเลือกใหม่จนกว่าจะเลือกตัวเลือกที่ถูกต้องที่สุด.

# เป็นการสร้างเมนูเลือกที่ผู้ใช้สามารถเลือกทำการกระทำต่าง ๆ กับโหนดของบล็อกเชนได้ โดยมีเลือกให้ผู้ใช้เลือกทำอย่างน้อย 5 การกระทำต่าง ๆ ได้:

# 1 Connect to a peer: ให้ผู้ใช้ป้อน host และ port ของโหนดเพื่อเชื่อมต่อกับโหนดพีร์อื่น ๆ ในเครือข่ายบล็อกเชน
#2 Create a transaction: ให้ผู้ใช้ป้อนที่อยู่วอลเล็ตของผู้รับและจำนวนเงินที่ต้องการส่ง เพื่อสร้างธุรกรรมใหม่บนเครือข่าย
# 3 View all transactions: แสดงรายการธุรกรรมทั้งหมดที่โหนดนี้เคยบันทึกไว้
# 4 View my wallet address: แสดงที่อยู่วอลเล็ตของโหนดนี้
# 5 Exit: ออกจากโปรแกรม

    print("Exiting...")




# รับค่า port จาก command line arguments
# สร้างโหนดใหม่และเริ่มต้นการทำงานของโหนด
# มีเมนูสำหรับให้ผู้ใช้เลือกทำสิ่งต่างๆ เช่น เชื่อมต่อกับ peer, สร้างธุรกรรม, ดูรายการธุรกรรมทั้งหมด, ดูที่อยู่กระเป๋าเงิน, และออกจากโปรแกรม