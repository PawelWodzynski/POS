document.addEventListener('DOMContentLoaded', () => {
  const createProductModal = new bootstrap.Modal(document.getElementById('createProductModal'));
  const openModalBtn = document.getElementById('openCreateProductModalBtn');
  const createProductForm = document.getElementById('createProductForm');

  openModalBtn.addEventListener('click', () => {
    createProductForm.reset();
    createProductForm.productImage.value = 'https://placehold.co/200x200?text=Produkt';
    createProductModal.show();
  });

  createProductForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Gather form data
    const formData = new FormData(createProductForm);
    const product = {
      title: formData.get('title'),
      category: formData.get('category'),
      description: formData.get('description'),
      price: parseFloat(formData.get('price')),
      rating: {
        rate: parseFloat(formData.get('ratingRate')),
        count: 0
      },
      image: formData.get('image')
    };

    // Generate unique incremented ID based on existing products in localStorage
    let maxId = 0;
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith('product_')) {
        try {
          const p = JSON.parse(localStorage.getItem(key));
          if (p.id > maxId) maxId = p.id;
        } catch {}
      }
    }
    product.id = maxId + 1;

    try {
      const response = await fetch('/api/products/create_product_simulation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product)
      });
      if (!response.ok) {
        alert('Failed to create product');
        return;
      }
      const createdProduct = await response.json();

      // Add new product to localStorage with count === 0
      const productKey = `product_${createdProduct.id}`;
      localStorage.setItem(productKey, JSON.stringify(createdProduct));

      // Optionally, you can update UI or notify user
      // alert('Product created and added to localStorage with count 0');
      createProductModal.hide();
      // Refresh product select dropdown to include new product
      if (window.populateProductSelect) {
        window.populateProductSelect();
      }
    } catch (error) {
      console.error('Error creating product:', error);
      alert('Error creating product');
    }
  });
});
