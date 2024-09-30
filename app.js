const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const User = require('./models/User'); 
const authRoutes = require('./routes/auth');  // Import the auth routes
const cors = require('cors');



const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));  // Serve static files from the public directory
app.use(cors());  // Enable CORS for all routes
app.use(cors({ origin: 'http://localhost:5000' }));

// MongoDB Connection
mongoose.connect('mongodb://localhost:27017/Ai', {
    
})
.then(() => console.log('Connected to MongoDB'))
.catch((err) => console.log('Error connecting to MongoDB:', err));

// Use the auth routes
app.use('/', authRoutes);

// Root Route - Redirect to register page
app.get('/', (req, res) => {
    res.redirect('/register');
});

// Server
app.listen(8000, () => {
    console.log('Server running on http://localhost:8000');
    
});
