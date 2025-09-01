document.addEventListener('DOMContentLoaded', () => {
  const productsTableBody = document.querySelector('#productsTable tbody');
  const productSelect = document.getElementById('productSelect');
  const quantityInput = document.getElementById('quantityInput');
  const acceptButton = document.getElementById('acceptButton');

  // Load cart from localStorage or initialize empty array
  function loadCart() {
    const cartStr = localStorage.getItem('cart');
    if (cartStr) {
      try {
        return JSON.parse(cartStr);
      } catch (e) {
        console.error('Error parsing cart from localStorage', e);
        return [];
      }
    }
    return [];
  }

  // Save cart to localStorage
  function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
  }

  // Render the cart table rows
  function renderCartTable() {
    const cart = loadCart();
    productsTableBody.innerHTML = '';
    cart.forEach(item => {
      const row = document.createElement('tr');

      const productIdCell = document.createElement('td');
      productIdCell.textContent = item.productId;
      row.appendChild(productIdCell);

      const nameCell = document.createElement('td');
      nameCell.textContent = item.name;
      row.appendChild(nameCell);

      const countCell = document.createElement('td');
      countCell.textContent = item.quantity;
      row.appendChild(countCell);

      const priceCell = document.createElement('td');
      priceCell.textContent = item.price;
      row.appendChild(priceCell);

      const imageCell = document.createElement('td');
      const img = document.createElement('img');
      img.src = item.image;
      img.alt = item.name;
      img.style.width = '50px';
      imageCell.appendChild(img);
      row.appendChild(imageCell);

      productsTableBody.appendChild(row);
    });
  }

  // Find product details by productId from localStorage
  function getProductById(productId) {
    const productStr = localStorage.getItem(`product_${productId}`);
    if (!productStr) return null;
    try {
      return JSON.parse(productStr);
    } catch (e) {
      console.error('Error parsing product from localStorage', e);
      return null;
    }
  }

  // Add or update product in cart
  function addOrUpdateProductInCart(productId, count) {
    const cart = loadCart();
    const product = getProductById(productId);
    if (!product) {
      alert('Selected product not found in localStorage');
      return;
    }

    const existingItem = cart.find(item => item.productId === productId);
    if (existingItem) {
      existingItem.quantity += count;
    } else {
      cart.push({
        productId: product.id,
        quantity: count,
        name: product.title,
        price: product.price,
        image: product.image
      });
    }
    saveCart(cart);
    renderCartTable();
  }

  // On accept button click
  acceptButton.addEventListener('click', () => {
    const productId = parseInt(productSelect.value);
    const quantity = parseInt(quantityInput.value);
    if (isNaN(productId) || isNaN(quantity) || quantity <= 0) {
      alert('Please select a product and enter a valid quantity');
      return;
    }

    // Just add or update product in local cart, do not send request yet
    addOrUpdateProductInCart(productId, quantity);
  });

  // On enter delivery button click
  const enterDeliveryButton = document.getElementById('enterDeliveryButton');
  enterDeliveryButton.addEventListener('click', () => {
    const cart = loadCart();
    if (cart.length === 0) {
      alert('Cart is empty, nothing to deliver');
      return;
    }

    // Prepare data to send to backend: list of {productID, count}
    const dataToSend = cart.map(item => ({
      productID: item.productId,
      count: item.quantity
    }));

    fetch('/api/products/add_products_simulation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataToSend)
    })
      .then(response => response.json())
      .then(data => {
        // On success, update localStorage counts for each product by adding returned counts
        data.forEach(item => {
          const productKey = `product_${item.productID}`;
          const productStr = localStorage.getItem(productKey);
          if (!productStr) return;
          try {
            const product = JSON.parse(productStr);
            // Increase rating.count by item.count as a simulation of stock count update
            product.rating = product.rating || {};
            product.rating.count = (product.rating.count || 0) + item.count;
            // Save updated product back to localStorage
            localStorage.setItem(productKey, JSON.stringify(product));
          } catch (e) {
            console.error('Error updating product in localStorage', e);
          }
        });
        alert('Delivery entered and local product counts updated.');
        // Optionally clear cart after delivery
        localStorage.removeItem('cart');
        renderCartTable();
      })
      .catch(error => {
        console.error('Error sending delivery data to server:', error);
        alert('Failed to send delivery data to server');
      });
  });

  // Initial render of cart table
  renderCartTable();
});
