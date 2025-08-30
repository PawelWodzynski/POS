document.addEventListener('DOMContentLoaded', async () => {
  await fetchProducts();
  renderProductTiles();

  const searchInput = document.getElementById('product-search-input');
  let lastValue = '';

  searchInput.addEventListener('input', async () => {
    const currentValue = searchInput.value.trim();

    if (currentValue === lastValue) {
      return;
    }
    lastValue = currentValue;

    if (currentValue.length === 0) {
      // If input is empty, render all products
      renderProductTiles();
      return;
    }

    try {
      const response = await fetch('/api/products/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name: currentValue })
      });

      if (!response.ok) {
        console.error('Search request failed');
        return;
      }

      const data = await response.json();
      console.log('Search response:', data);

      // Filter products by name containing the search term (case-insensitive)
      const container = document.getElementById('product-tiles-container');
      container.innerHTML = '';

      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key.startsWith('product_')) {
          try {
            const product = JSON.parse(localStorage.getItem(key));
            if (product && product.title.toLowerCase().includes(currentValue.toLowerCase())) {
              // tutaj możesz ponownie wyrenderować kafelek produktu
              // żeby nie duplikować całego kodu, możesz wyciągnąć renderowanie pojedynczego produktu do funkcji pomocniczej
            }
          } catch (e) {
            console.error('Failed to parse product from localStorage key:', key, e);
          }
        }
      }
    } catch (err) {
      console.error('Error during product search:', err);
    }
  });
});
