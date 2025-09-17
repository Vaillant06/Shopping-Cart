// ------------------ Product Data ------------------
const products = [
  { name: "Samsung Galaxy S24 Ultra", price: 129999, image: "static/images/samsung.avif" },
  { name: "Apple iPhone 15 Pro", price: 134900, image: "static/images/iphone.avif" },
  { name: "OnePlus 12R", price: 42999, image: "static/images/oneplus.avif" },
  { name: "Realme Narzo 60x", price: 17499, image: "static/images/realme.avif" },
  { name: "Dell Inspiron 15 Laptop", price: 58990, image: "static/images/dell.avif" },
  { name: "MacBook Air M2", price: 104900, image: "static/images/macbook.avif" },
  { name: "HP Pavilion Gaming Laptop", price: 74999, image: "static/images/hp.avif" },
  { name: "Acer VivoBook 16", price: 148000, image: "static/images/acer.avif" },
  { name: "Sony WH-1000XM5 Headphones", price: 29990, image: "static/images/headphones.avif" },
  { name: "boAt Airdopes 141", price: 1499, image: "static/images/earbuds.avif" },
  { name: "JBL Flip 6 Bluetooth Speaker", price: 11499, image: "static/images/speaker.avif" },
  { name: "Samsung 55in 4K Smart TV", price: 52990, image: "static/images/tv.avif" },
  { name: "LG 1.5 Ton Split AC", price: 45990, image: "static/images/ac.avif" },
  { name: "Whirlpool Double Door Fridge", price: 28990, image: "static/images/fridge.avif" },
  { name: "Bosch 7kg Washing Machine", price: 32990, image: "static/images/wm.avif" },
  { name: "Canon EOS 1500D DSLR", price: 38990, image: "static/images/camera.avif" },
  { name: "Nike Air Max Shoes", price: 8499, image: "static/images/nike.avif" },
  { name: "Adidas Ultraboost", price: 12999, image: "static/images/adidas.avif" },
  { name: "Puma Sports T-Shirt", price: 1499, image: "static/images/tshirt.avif" },
  { name: "Levi's Slim Fit Jeans", price: 3499, image: "static/images/jeans.avif" },
  { name: "Fossil Gen 6 Smartwatch", price: 22990, image: "static/images/watch.avif" },
  { name: "Apple Watch SE", price: 29900, image: "static/images/swatch.avif" },
  { name: "Cosmic Byte Gaming Keyboard", price: 2499, image: "static/images/keyboard.avif" },
  { name: "Logitech MX Master 3 Mouse", price: 8499, image: "static/images/mouse.avif" }
];

// ------------------ Render Products ------------------
const productList = document.getElementById("product-list");

products.forEach(product => {
  productList.innerHTML += `
    <div class="col-sm-3">
      <div class="card mt-3 mb-3 d-block mx-auto">
        <img src="${product.image}" alt="${product.name}" class="card-img-top">
        <div class="card-content">
          <h5 class="card-title mt-3">${product.name}</h5>
          <p class="card-description">Price: Rs. ${product.price.toLocaleString()}</p>
          <div class="quantity mb-3">
            <h6>Quantity</h6>
            <div class="quantity-button">
              <button class="btn btn-outline-secondary">-</button>
              <span class="count">1</span>
              <button class="btn btn-outline-secondary">+</button>
            </div>
          </div>
          <form action="/add_to_cart" method="POST">
            <input type="hidden" name="name" value="${product.name}">
            <input type="hidden" name="price" value="${product.price}">
            <input type="hidden" name="quantity" class="quantity-input" value="1">
            <button type="submit" class="btn btn-outline-success d-block mx-auto mt-3 mb-3 p-2">
              Add To Cart
            </button>
          </form>
        </div>
      </div>
    </div>
  `;
});

function attachQuantityHandlers(card) {
  const minusBtn = card.querySelector(".quantity-button button:first-child");
  const plusBtn = card.querySelector(".quantity-button button:last-child");
  const countSpan = card.querySelector(".count");
  const quantityInput = card.querySelector(".quantity-input");

  let count = 1;

  minusBtn.addEventListener("click", () => {
    if (count > 1) {
      count--;
      countSpan.textContent = count;
      quantityInput.value = count;
    }
  });

  plusBtn.addEventListener("click", () => {
    count++;
    countSpan.textContent = count;
    quantityInput.value = count;
  });
}

// ------------------ Apply Handlers ------------------
document.querySelectorAll(".card").forEach(card => {
  attachQuantityHandlers(card);
});