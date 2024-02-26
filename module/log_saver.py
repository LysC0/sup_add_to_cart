import csv

def log_csv (title, size, color, cart_url):
     with open('log.csv', 'a', newline='') as f:
        data = {'title': title, 'size': size, 'color' : color, 'cart url' : cart_url}
        writer = csv.DictWriter(f, fieldnames=data.keys())
    
        if f.tell() == 0:
            writer.writeheader()

        writer.writerow(data)
        f.close()