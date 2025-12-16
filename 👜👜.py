import requests
import concurrent.futures
import time
import sys
import os
import webbrowser

class FastProxyChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.working = []
        webbrowser.open("https://t.me/NARUTO_CODEX")
        
    def NARUTO_check_proxy(self, proxy):
        proxy_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        
        try:
            start = time.time()
            response = self.session.get(
                'http://httpbin.org/ip',
                proxies=proxy_dict,
                timeout=5
            )
            response_time = round((time.time() - start) * 1000)
            
            if response.status_code == 200:
                return {
                    'proxy': proxy,
                    'status': '✅',
                    'time': response_time,
                    'ip': response.json().get('origin', 'Unknown')
                }
        except:
            pass
            
        return {
            'proxy': proxy,
            'status': '❌',
            'time': 0,
            'ip': None
        }

    def NARUTO_check_all(self, proxies, max_workers=20):
        print(f"🔍 فحص {len(proxies)} بروكسي...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.NARUTO_check_proxy, proxies))
        
        for result in results:
            if result['status'] == '✅':
                self.working.append(result)
                print(f"✅ {result['proxy']} - {result['time']}ms - {result['ip']}")
            else:
                print(f"❌ {result['proxy']}")
        
        return results

def NARUTO_load_proxies_from_file(filename):
    if not os.path.exists(filename):
        return []
    
    with open(filename, 'r', encoding='utf-8') as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    return proxies

def NARUTO_save_working_proxies(proxies, filename='working_proxies.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for proxy in proxies:
            f.write(f"{proxy['proxy']}\n")
    return filename

def main():
    print("🚀 فحص البروكسيات السريع")
    print("=" * 50)
    
    print("\n📁 اختر مصدر البروكسيات:")
    print("1 - استخدام القائمة الافتراضية")
    print("2 - تحميل من ملف")
    print("3 - إدخال يدوي")
    
    choice = input("\nاختر الخيار (1/2/3): ").strip()
    
    proxies = []
    
    if choice == "1":
        proxies = [
            "103.79.96.218:4153", "178.210.130.89:5678", "179.191.114.65:4153",
            "103.148.113.73:8199", "140.235.169.62:8085", "203.194.21.241:4153",
            "139.59.234.208:50929", "42.200.253.116:8080", "194.39.254.35:80",
            "8.218.136.43:1011", "47.238.134.126:81", "193.202.16.91:8085",
            "8.213.222.157:8081", "117.4.107.199:51796", "65.21.34.102:80",
            "199.229.254.129:4145", "45.115.113.169:11011", "103.247.13.54:8080",
            "118.163.120.181:58837", "184.181.217.206:4145", "8.210.27.75:1011",
            "149.28.13.113:10786", "93.90.212.2:4153", "72.207.113.97:4145",
            "185.216.105.237:6814", "186.215.87.194:30008", "190.104.219.149:4153",
            "177.44.18.96:4145", "200.75.137.210:4145", "172.67.193.120:80",
            "203.32.120.50:80"
        ]
        
    elif choice == "2":
        filename = input("أدخل اسم الملف (مثال: proxies.txt): ").strip()
        proxies = NARUTO_load_proxies_from_file(filename)
        if not proxies:
            print("❌ لم يتم العثور على بروكسيات في الملف")
            return
            
    elif choice == "3":
        print("أدخل البروكسيات (افصل بينها بفاصلة أو سطر جديد، اضغط Enter مرتين للبدء):")
        input_lines = []
        while True:
            line = input().strip()
            if line == "":
                if input_lines:
                    break
                else:
                    continue
            input_lines.append(line)
        
        proxies = []
        for line in input_lines:
            new_proxies = [p.strip() for p in line.replace(',', '\n').split('\n') if p.strip()]
            proxies.extend(new_proxies)
    
    else:
        print("❌ اختيار غير صحيح")
        return
    
    if not proxies:
        print("❌ لا توجد بروكسيات للفحص")
        return
    
    try:
        max_workers = int(input(f"\n🧵 أدخل عدد الثreads للفحص (افتراضي 20): ") or "20")
    except:
        max_workers = 20
    
    checker = FastProxyChecker()
    
    print(f"\n📊 بدء فحص {len(proxies)} بروكسي...")
    print("⏳ يرجى الانتظار...\n")
    
    start_time = time.time()
    results = checker.NARUTO_check_all(proxies, max_workers)
    total_time = time.time() - start_time
    
    working_count = len(checker.working)
    total_count = len(proxies)
    
    print(f"\n{'='*50}")
    print("📊 النتائج النهائية:")
    print(f"✅ البروكسيات الشغالة: {working_count}")
    print(f"❌ البروكسيات الفاشلة: {total_count - working_count}")
    print(f"📈 نسبة النجاح: {(working_count/total_count)*100:.1f}%")
    print(f"⏱️ وقت الفحص: {total_time:.2f} ثانية")
    
    if checker.working:
        print(f"\n🎯 البروكسيات الشغالة (مُرتبة حسب السرعة):")
        sorted_working = sorted(checker.working, key=lambda x: x['time'])
        
        for i, proxy in enumerate(sorted_working, 1):
            print(f"{i:2d}. 🌐 {proxy['proxy']} - ⏱️ {proxy['time']}ms - 📍 {proxy['ip']}")
        
        save = input("\n💾 هل تريد حفظ البروكسيات الشغالة؟ (y/n): ").lower()
        if save == 'y':
            filename = NARUTO_save_working_proxies(sorted_working)
            print(f"✅ تم الحفظ في {filename}")
            
            print(f"\n🏆 أفضل 5 بروكسيات:")
            for i, proxy in enumerate(sorted_working[:5], 1):
                print(f"{i}. {proxy['proxy']} - {proxy['time']}ms")
    else:
        print("\n⚠️ لم يتم العثور على أي بروكسيات شغالة")

if __name__ == "__main__":
    main()