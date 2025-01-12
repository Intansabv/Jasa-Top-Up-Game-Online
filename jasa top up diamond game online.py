from typing import Optional, List, Dict
from datetime import datetime
import random

# Array untuk menyimpan daftar paket diamond
class DiamondPackage:
    def __init__(self, id: int, jumlah: int, harga: float):
        self.id = id
        self.jumlah = jumlah
        self.harga = harga

# Queue untuk antrian transaksi
class TransactionNode:
    def __init__(self, user_id: str, package: DiamondPackage, timestamp: datetime):
        self.user_id = user_id
        self.package = package
        self.timestamp = timestamp
        self.next = None

class TransactionQueue:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, transaction: TransactionNode):
        if self.rear is None:
            self.front = self.rear = transaction
        else:
            self.rear.next = transaction
            self.rear = transaction
    
    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return temp

# Perulangan while di display_queue    
    def display_queue(self):
        if self.is_empty():
            print("Tidak ada transaksi dalam antrian")
            return
        
        current = self.front
        print("\nDaftar Antrian Transaksi:")
        print("ID Pengguna | Jumlah Diamond | Harga | Waktu")
        print("-" * 60)
        while current:
            print(f"{current.user_id} | {current.package.jumlah:13d} | Rp {current.package.harga:,} | {current.timestamp.strftime('%H:%M:%S')}")
            current = current.next

    def process_queue(self):
        if self.is_empty():
            print("Tidak ada transaksi untuk diproses")
            return
        
        count = 0
        while not self.is_empty():
            transaction = self.dequeue()
            print(f"Memproses transaksi: {transaction.package.jumlah} diamond untuk ID {transaction.user_id}")
            count += 1
        
        print(f"\nBerhasil memproses {count} transaksi!")

# Binary Search Tree untuk Mentimpan Riwayat Pembelian
class HistoryNode:
    def __init__(self, user_id: str, total_spent: float):
        self.user_id = user_id
        self.total_spent = total_spent
        self.left = None
        self.right = None

class UserHistoryTree:
    def __init__(self):
        self.root = None
    
    def insert(self, user_id: str, amount: float):
        if not self.root:
            self.root = HistoryNode(user_id, amount)
        else:
            self._insert_recursive(self.root, user_id, amount)
    
    def _insert_recursive(self, node: HistoryNode, user_id: str, amount: float):
        if user_id < node.user_id:
            if node.left is None:
                node.left = HistoryNode(user_id, amount)
            else:
                self._insert_recursive(node.left, user_id, amount)
        else:
            if node.right is None:
                node.right = HistoryNode(user_id, amount)
            else:
                self._insert_recursive(node.right, user_id, amount)
    
    def display_history(self):
        if not self.root:
            print("Tidak ada riwayat pembelian")
            return
        print("\nRiwayat Pembelian User (BST):")
        self._display_recursive(self.root)
    
    def _display_recursive(self, node: HistoryNode):
        if node:
            self._display_recursive(node.left)
            print(f"User ID: {node.user_id}, Total Pembelian: Rp {node.total_spent:,}")
            self._display_recursive(node.right)

# Graph untuk Rekomendasi Paket
class PackageGraph:
    def __init__(self):
        self.adjacency_list: Dict[int, List[tuple]] = {}
    
    def add_package_relation(self, pkg1_id: int, pkg2_id: int, weight: float):
        if pkg1_id not in self.adjacency_list:
            self.adjacency_list[pkg1_id] = []
        if pkg2_id not in self.adjacency_list:
            self.adjacency_list[pkg2_id] = []
        
        self.adjacency_list[pkg1_id].append((pkg2_id, weight))
        self.adjacency_list[pkg2_id].append((pkg1_id, weight))
    
    def get_recommendations(self, package_id: int, num_recommendations: int = 3) -> List[int]:
        if package_id not in self.adjacency_list:
            return []
        
        neighbors = sorted(self.adjacency_list[package_id], key=lambda x: x[1], reverse=True)
        return [pkg_id for pkg_id, _ in neighbors[:num_recommendations]]


class EnhancedTopUpSystem:
    def __init__(self):
        # Array untuk paket diamond
        self.packages = [
            DiamondPackage(1, 100, 15000),
            DiamondPackage(2, 70, 9000),
            DiamondPackage(3, 500, 72000),
            DiamondPackage(4, 1000, 127000),
            DiamondPackage(5, 1075, 137000),
            DiamondPackage(6, 720, 91000),
            DiamondPackage(7, 200, 29000),
            DiamondPackage(8, 355, 45000),
            DiamondPackage(9, 860, 109000)
        ]
        self.transaction_queue = TransactionQueue()
        self.user_history = UserHistoryTree()
        self.package_graph = PackageGraph()
        self._initialize_package_graph()
    
    def _initialize_package_graph(self):
        for i, pkg1 in enumerate(self.packages):
            for pkg2 in self.packages[i+1:]:
                price_diff = abs(pkg1.harga - pkg2.harga)
                similarity = 1 / (1 + price_diff/1000) 
                self.package_graph.add_package_relation(pkg1.id, pkg2.id, similarity)


    def validate_user_id(self, user_id: str) -> bool:
        return user_id.isdigit() and 9 <= len(user_id) <= 10
    
    def search_package(self, package_id: int) -> Optional[DiamondPackage]:
        for package in self.packages:
            if package.id == package_id:
                return package
        return None
    
 # Perulangan for di bubble sort   
    def sort_packages_by_price(self):
        n = len(self.packages)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.packages[j].harga > self.packages[j + 1].harga:
                    self.packages[j], self.packages[j + 1] = self.packages[j + 1], self.packages[j]

# Percabangan di process_transaction    
    def process_transaction(self, user_id: str, package_id: int) -> bool:
        if not self.validate_user_id(user_id):
            print("ID pengguna tidak valid!")
            return False
        
        package = self.search_package(package_id)
        if not package:
            print("Paket diamond tidak ditemukan!")
            return False
        
        transaction = TransactionNode(user_id, package, datetime.now())
        self.transaction_queue.enqueue(transaction)
        self.user_history.insert(user_id, package.harga)
        
        print(f"Transaksi berhasil ditambahkan ke antrian! {package.jumlah} diamond akan ditambahkan ke ID {user_id}")
        return True

    def display_packages(self):
        print("\nDaftar Paket Diamond:")
        print("ID  | Jumlah Diamond | Harga")
        print("-" * 30)
        for package in self.packages:
            print(f"{package.id}   | {package.jumlah:13d} | Rp {package.harga:,}")
    
    def display_recommendations(self, package_id: int):
        recommendations = self.package_graph.get_recommendations(package_id)
        if recommendations:
            print("\nRekomendasi Paket Serupa:")
            for pkg_id in recommendations:
                package = self.search_package(pkg_id)
                print(f"- {package.jumlah} diamond (Rp {package.harga:,})")
        else:
            print("Tidak ada rekomendasi untuk paket ini")

def main():
    system = EnhancedTopUpSystem()

 # Perulangan while di menu utama   
    while True:
        print("\n=== Top Up Diamond Free Fire via ID MOCHI STORE===")
        print("\n===List Menu===")
        print("1. Lihat Paket Diamond")
        print("2. Top Up Diamond")
        print("3. Urutkan Paket berdasarkan Harga")
        print("4. Lihat Antrian Transaksi")
        print("5. Proses Semua Transaksi")
        print("6. Lihat Riwayat Pembelian User")
        print("7. Lihat Rekomendasi Paket")
        print("8. Keluar")
        
        choice = input("Pilih menu (1-8): ")

    # Percabangan if-else di menu utama    
        if choice == "1":
            system.display_packages()
        
        elif choice == "2":
            user_id = input("Masukkan ID Free Fire (9-10 digit): ")
            system.display_packages()
            try:
                package_id = int(input("Pilih ID paket: "))
                system.process_transaction(user_id, package_id)
            except ValueError:
                print("ID paket harus berupa angka!")
        
        elif choice == "3":
            system.sort_packages_by_price()
            print("Paket telah diurutkan berdasarkan harga!")
            system.display_packages()
        
        elif choice == "4":
            system.transaction_queue.display_queue()
        
        elif choice == "5":
            system.transaction_queue.process_queue()
        
        elif choice == "6":
            system.user_history.display_history()
        
        elif choice == "7":
            system.display_packages()
            try:
                package_id = int(input("Masukkan ID paket untuk melihat rekomendasi: "))
                system.display_recommendations(package_id)
            except ValueError:
                print("ID paket harus berupa angka!")
        
        elif choice == "8":
            print("Terima kasih telah Top Up di MOCHI STORE:)")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
