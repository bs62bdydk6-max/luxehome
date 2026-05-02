from flask import Flask, render_template_string

app = Flask(__name__)

# ПРОВЕРЕННАЯ БАЗА ТОВАРОВ
PRODUCTS = [
    {"id": 1, "name": "Диван 'Chesterfield'", "price": 380000, "img": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800", "desc": "Премиальная изумрудная кожа, массив бука и классическая стяжка. Символ вашего статуса."},
    {"id": 2, "name": "Кресло 'Emerald'", "price": 95000, "img": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800", "desc": "Глубокое кресло из мягкого велюра. Создано для долгих вечеров с книгой."},
    {"id": 3, "name": "Стол 'Loft Oak'", "price": 145000, "img": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=800", "desc": "Цельный спил дуба на стальном подстолье. Индустриальный шик в вашем доме."},
    {"id": 4, "name": "Стул 'Minimal Grey'", "price": 35000, "img": "https://images.unsplash.com/photo-1503602642458-232111445657?w=800", "desc": "Эргономика и стиль. Идеальное решение для современной столовой."},
    {"id": 5, "name": "Тумба 'Industrial'", "price": 68000, "img": "https://images.unsplash.com/photo-1532372320978-9b4d00970021?w=800", "desc": "Сочетание брутального металла и теплого дерева. Практичное искусство."},
    {"id": 6, "name": "Зеркало 'Sun Gold'", "price": 52000, "img": "https://images.unsplash.com/photo-1618220252344-8ec99ec624b1?w=800", "desc": "Золотая оправа ручной работы. Визуально расширяет пространство и добавляет света."}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LUXEHOME | Мебель Владислава</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@300;600;900&display=swap');
        body { font-family: 'Inter', sans-serif; transition: 0.5s; background: #fff; scroll-behavior: smooth; }
        .unbounded { font-family: 'Unbounded', sans-serif; }
        .dark { background: #080808; color: white; }
        
        /* 3D Эффект карточек */
        .card-3d { transition: transform 0.5s cubic-bezier(0.2, 1, 0.3, 1); perspective: 1000px; }
        .card-3d:hover { transform: translateY(-10px) rotateX(5deg) rotateY(2deg); }
        
        /* Баннер */
        .hero { height: 70vh; background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=1600'); background-size: cover; background-position: center; border-radius: 0 0 80px 80px; }
        
        /* Модалки и Корзина */
        .modal, .cart-sidebar { display: none; position: fixed; inset: 0; z-index: 1000; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); align-items: center; justify-content: center; }
        .modal-content { max-width: 900px; width: 95%; background: white; border-radius: 40px; overflow: hidden; display: flex; animation: slideUp 0.4s ease; }
        .dark .modal-content { background: #151515; }
        .cart-window { position: absolute; right: 0; top: 0; width: 400px; height: 100%; background: white; padding: 40px; box-shadow: -10px 0 30px rgba(0,0,0,0.3); }
        .dark .cart-window { background: #111; }
        
        @keyframes slideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @media (max-width: 768px) { .modal-content { flex-direction: column; } .hero { border-radius: 0 0 40px 40px; } }
    </style>
</head>
<body id="body">

    <header class="fixed top-0 w-full z-50 p-6 flex justify-between items-center bg-white/70 dark:bg-black/70 backdrop-blur-md">
        <h1 class="unbounded text-xl font-black text-indigo-500 italic tracking-tighter uppercase">LUXEHOME</h1>
        <div class="flex items-center gap-6">
            <button onclick="document.getElementById('body').classList.toggle('dark')" class="text-xl">🌓</button>
            <button onclick="toggleCart()" class="bg-black text-white dark:bg-white dark:text-black rounded-full px-6 py-2 text-[10px] font-black uppercase tracking-widest">
                Корзина (<span id="count">0</span>)
            </button>
        </div>
    </header>

    <section class="hero flex items-center justify-center text-center text-white px-4">
        <div>
            <p class="uppercase tracking-[0.4em] text-[10px] mb-4 font-bold">Эксклюзивная коллекция</p>
            <h2 class="unbounded text-5xl md:text-8xl font-black mb-8 leading-none">LUXEHOME</h2>
            <a href="#catalog" class="inline-block border-2 border-white px-10 py-4 rounded-full font-bold uppercase text-[10px] hover:bg-white hover:text-black transition">Смотреть каталог</a>
        </div>
    </section>

    <section class="py-24 px-10 max-w-4xl mx-auto text-center">
        <h3 class="unbounded text-2xl mb-8 font-black uppercase tracking-tighter">Манифест качества</h3>
        <p class="text-gray-500 dark:text-gray-400 italic text-lg leading-relaxed">«Мебель — это не просто предметы. Это характер вашего дома. В LUXEHOME мы под руководством Владислава создаем вещи, которые служат поколениям». </p>
    </section>

    <main id="catalog" class="max-w-7xl mx-auto p-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-16">
        {% for p in products %}
        <div class="card-3d cursor-pointer group" onclick='openProduct({{ p|tojson }})'>
            <div class="rounded-[40px] overflow-hidden mb-6 shadow-xl aspect-[4/5] bg-gray-100">
                <img src="{{ p.img }}" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
            </div>
            <div class="px-2">
                <h3 class="unbounded text-lg font-bold mb-1 uppercase">{{ p.name }}</h3>
                <p class="text-indigo-600 font-black text-2xl tracking-tighter">{{ "{:,}".format(p.price).replace(",", " ") }} ₸</p>
            </div>
        </div>
        {% endfor %}
    </main>

    <div id="productModal" class="modal px-4" onclick="toggleModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <img id="m-img" src="" class="w-full md:w-1/2 h-[500px] object-cover">
            <div class="p-12 flex flex-col justify-center">
                <h2 id="m-name" class="unbounded text-3xl font-black mb-6 uppercase tracking-tighter"></h2>
                <p id="m-desc" class="text-gray-500 dark:text-gray-400 mb-8 leading-relaxed"></p>
                <p id="m-price" class="text-indigo-600 font-black text-4xl mb-10 italic"></p>
                <button id="m-add" class="bg-indigo-600 text-white py-5 rounded-2xl font-black uppercase tracking-widest hover:bg-black transition shadow-xl">В корзину</button>
            </div>
        </div>
    </div>

    <div id="cartOverlay" class="modal" onclick="toggleCart()">
        <div class="cart-window flex flex-col" onclick="event.stopPropagation()">
            <div class="flex justify-between items-center mb-10">
                <h2 class="unbounded text-2xl font-black italic">КОРЗИНА</h2>
                <button onclick="toggleCart()" class="text-3xl">&times;</button>
            </div>
            <div id="cartList" class="flex-1 overflow-y-auto space-y-6"></div>
            <div class="border-t pt-8 mt-8">
                <div class="flex justify-between text-2xl font-black mb-8 italic text-indigo-500">
                    <span>ИТОГО:</span>
                    <span id="totalSum">0</span>
                </div>
                <button onclick="alert('Заказ оформлен! Владислав свяжется с вами.')" class="w-full bg-black dark:bg-indigo-600 text-white py-6 rounded-2xl font-black uppercase tracking-widest transition">Оформить заказ</button>
            </div>
        </div>
    </div>

    <script>
        let cart = [];
        function openProduct(p) {
            document.getElementById('m-img').src = p.img;
            document.getElementById('m-name').innerText = p.name;
            document.getElementById('m-desc').innerText = p.desc;
            document.getElementById('m-price').innerText = p.price.toLocaleString('ru-RU') + ' ₸';
            document.getElementById('m-add').onclick = () => { cart.push(p); updateUI(); toggleModal(); };
            toggleModal();
        }
        function toggleModal() {
            const m = document.getElementById('productModal');
            m.style.display = m.style.display === 'flex' ? 'none' : 'flex';
        }
        function toggleCart() {
            const c = document.getElementById('cartOverlay');
            c.style.display = c.style.display === 'flex' ? 'none' : 'flex';
        }
        function updateUI() {
            document.getElementById('count').innerText = cart.length;
            const list = document.getElementById('cartList');
            list.innerHTML = cart.map((item, i) => `
                <div class="flex items-center gap-4 bg-gray-50 dark:bg-zinc-900 p-4 rounded-3xl">
                    <img src="${item.img}" class="w-16 h-16 rounded-xl object-cover">
                    <div class="flex-1">
                        <div class="font-bold text-[10px] uppercase">${item.name}</div>
                        <div class="text-indigo-500 font-bold">${item.price.toLocaleString('ru-RU')} ₸</div>
                    </div>
                    <button onclick="cart.splice(${i}, 1); updateUI()" class="text-red-500 font-bold">×</button>
                </div>
            `).join('');
            const sum = cart.reduce((s, i) => s + i.price, 0);
            document.getElementById('totalSum').innerText = sum.toLocaleString('ru-RU') + ' ₸';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, products=PRODUCTS)

if __name__ == '__main__':
    app.run(debug=True)