document.addEventListener('DOMContentLoaded', () => {
  const productSelect = document.getElementById('productSelect');

  // Load products from localStorage keys starting with "product_"
  function loadProducts() {
    const products = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('product_')) {
        try {
          const product = JSON.parse(localStorage.getItem(key));
          products.push(product);
        } catch (e) {
          console.error('Error parsing product from localStorage', key, e);
        }
      }
    }
    return products;
  }

  // Populate the select dropdown with products
  function populateProductSelect() {
    const products = loadProducts();
    productSelect.innerHTML = '';
    products.forEach(product => {
      const option = document.createElement('option');
      option.value = product.id;
      option.textContent = `${product.title} (ID: ${product.id})`;
      productSelect.appendChild(option);
    });
  }

  populateProductSelect();
});
