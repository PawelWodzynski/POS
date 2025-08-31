/**
 * cart.js
 * Handles cart quantity modifications and synchronizes product and cart localStorage.
 */

// Helper function to get cart from localStorage
function getCart() {
  return JSON.parse(localStorage.getItem('cart')) || [];
}

// Helper function to save cart to localStorage
function saveCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

// Helper function to get product by id from localStorage
function getProduct(id) {
  return JSON.parse(localStorage.getItem('product_' + id));
}

// Helper function to save product to localStorage
function saveProduct(product) {
  localStorage.setItem('product_' + product.id, JSON.stringify(product));
}

// Function to handle DELETE response: add 1 product to product localStorage, decrement quantity or remove from cart localStorage
function handleDeleteProduct(productId) {
  console.log('handleDeleteProduct called for productId:', productId);
  let cart = getCart();
  let product = getProduct(productId);
  console.log('Product before increment:', product);

  // Add 1 product quantity to product localStorage
  if (product && product.rating && typeof product.rating.count === 'number') {
    product.rating.count += 1;
    saveProduct(product);
    console.log('Product after increment:', product);
  } else {
    console.warn('Product or product.rating.count invalid for productId:', productId);
  }

  // Decrement quantity or remove product from cart localStorage
  const cartItemIndex = cart.findIndex(item => item.productId === productId);
  if (cartItemIndex !== -1) {
    if (cart[cartItemIndex].quantity > 1) {
      cart[cartItemIndex].quantity -= 1;
    } else {
      cart.splice(cartItemIndex, 1);
    }
    saveCart(cart);
  } else {
    console.warn('Product not found in cart for productId:', productId);
  }
}

// Function to handle PUT response: add 1 product to cart localStorage, remove 1 product from product localStorage
function handlePutProduct(productId) {
  console.log('handlePutProduct called for productId:', productId);
  let cart = getCart();
  let product = getProduct(productId);
  console.log('Product before decrement:', product);

  // Add 1 product quantity to cart localStorage
  const cartItem = cart.find(item => item.productId === productId);
  if (cartItem) {
    cartItem.quantity += 1;
  } else {
    cart.push({ productId: productId, quantity: 1 });
  }
  saveCart(cart);

  // Remove 1 product quantity from product localStorage
  if (product && product.rating && typeof product.rating.count === 'number' && product.rating.count > 0) {
    product.rating.count -= 1;
    saveProduct(product);
    console.log('Product after decrement:', product);
  } else {
    console.warn('Product or product.rating.count invalid or zero for productId:', productId);
  }
}

// Export functions if using modules (optional)
// export { handleDeleteProduct, handlePutProduct };
