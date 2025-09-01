document.addEventListener('DOMContentLoaded', () => {
  // Delay modal initialization until the modal element is fully available
  const openModalBtn = document.getElementById('openCreateProductModalBtn');
  let createProductForm = null;
  let createProductModal = null;

  openModalBtn.addEventListener('click', () => {
    if (!createProductModal) {
      const modalElement = document.getElementById('createProductModal');
      if (!modalElement) {
        console.error('Modal element with id "createProductModal" not found.');
        return;
      }
      createProductModal = new bootstrap.Modal(modalElement);
    }
    if (!createProductForm) {
      createProductForm = document.getElementById('createProductForm');
      if (!createProductForm) {
        console.error('Form element with id "createProductForm" not found.');
        return;
      }
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
          if (createProductModal) {
            createProductModal.hide();
          }
          // Refresh product select dropdown to include new product
          if (window.populateProductSelect) {
            window.populateProductSelect();
          }
        } catch (error) {
          console.error('Error creating product:', error);
          alert('Error creating product');
        }
      });
    }
    createProductForm.reset();
    createProductForm.productImage.value = 'https://placehold.co/200x200?text=Produkt';

    // Populate category dropdown dynamically
    const categorySelect = document.getElementById('productCategory');
    categorySelect.innerHTML = '';
    const categoriesStr = localStorage.getItem('fakestore_categories');
    let categories = [];
    if (categoriesStr) {
      try {
        categories = JSON.parse(categoriesStr);
      } catch (e) {
        console.error('Failed to parse fakestore_categories from localStorage', e);
      }
    }
    categories.forEach(cat => {
      const option = document.createElement('option');
      option.value = cat;
      option.textContent = cat;
      categorySelect.appendChild(option);
    });

    createProductModal.show();
  });
});
