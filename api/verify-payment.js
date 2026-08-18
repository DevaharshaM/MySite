const crypto = require('crypto');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
  const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = body || {};

  if (!razorpay_order_id || !razorpay_payment_id || !razorpay_signature) {
    return res.status(400).json({ error: 'Missing required payment details' });
  }

  const secret = process.env.RAZORPAY_KEY_SECRET?.trim().replace(/['"]/g, '');
  if (!secret) {
    console.error('RAZORPAY_KEY_SECRET is not configured on the server');
    return res.status(500).json({ error: 'Internal server configuration error' });
  }

  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(`${razorpay_order_id}|${razorpay_payment_id}`);
  const generatedSignature = hmac.digest('hex');

  if (generatedSignature === razorpay_signature) {
    return res.status(200).json({ status: 'success', message: 'Payment verified successfully' });
  } else {
    return res.status(400).json({ error: 'Payment signature verification failed' });
  }
};
