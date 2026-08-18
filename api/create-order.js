const Razorpay = require('razorpay');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  const { amount, currency } = body || {};

  if (!amount || isNaN(amount)) {
    return res.status(400).json({ error: 'Valid amount is required' });
  }

  const numericAmount = parseFloat(amount);
  if (numericAmount < 1 || numericAmount > 100000) {
    return res.status(400).json({ error: 'Amount must be between 1 and 100,000' });
  }

  const amountInPaise = Math.round(numericAmount * 100);
  const selectedCurrency = (currency && typeof currency === 'string') ? currency.toUpperCase() : 'INR';

  try {
    const keyId = process.env.RAZORPAY_KEY_ID?.trim().replace(/['"]/g, '');
    const keySecret = process.env.RAZORPAY_KEY_SECRET?.trim().replace(/['"]/g, '');

    if (!keyId || !keySecret) {
      console.error('Razorpay credentials are not fully configured in environment');
      return res.status(500).json({ error: 'Payment gateway configuration error' });
    }

    const razorpay = new Razorpay({
      key_id: keyId,
      key_secret: keySecret,
    });

    const options = {
      amount: amountInPaise,
      currency: selectedCurrency,
      receipt: `receipt_order_${Date.now()}`,
    };

    const order = await razorpay.orders.create(options);
    return res.status(200).json({
      order_id: order.id,
      amount: order.amount,
      currency: order.currency,
      key_id: keyId,
    });
  } catch (error) {
    console.error('Error creating Razorpay order:', error);
    return res.status(500).json({ error: 'Failed to create order. Please try again.' });
  }
};
