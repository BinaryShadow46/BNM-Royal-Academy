// Admin Panel JavaScript

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar navigation
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') {
                e.preventDefault();
            }
            
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Update dashboard content based on selection
            updateDashboardContent(this.textContent.trim());
        });
    });
    
    // Quick action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.querySelector('span').textContent;
            alert(`Action: ${action}\nThis would open a modal/form in production version.`);
        });
    });
    
    // Notification bell
    const notificationBell = document.querySelector('.notification');
    notificationBell.addEventListener('click', function() {
        alert('You have 3 notifications:\n1. New student registration\n2. Fee payment overdue\n3. Staff meeting reminder');
    });
    
    // Search functionality
    const searchInput = document.querySelector('.search-box input');
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            alert(`Searching for: "${this.value}"\nResults would appear here in production.`);
            this.value = '';
        }
    });
    
    // Logout button
    const logoutBtn = document.querySelector('.logout');
    logoutBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to logout?')) {
            window.location.href = '/index.html';
        }
    });
});

// Update dashboard content based on selection
function updateDashboardContent(section) {
    const dashboardTitle = document.querySelector('.dashboard-content h1');
    const dashboardContent = document.querySelector('.dashboard-content > div:first-child');
    
    // In a full implementation, this would load different content
    // For now, just update the title
    if (section !== 'Dashboard') {
        dashboardTitle.textContent = `${section} Management`;
        
        // Show a message that this is a demo
        if (!document.querySelector('.demo-message')) {
            const demoMsg = document.createElement('div');
            demoMsg.className = 'demo-message';
            demoMsg.style.background = '#f8f9fa';
            demoMsg.style.padding = '2rem';
            demoMsg.style.textAlign = 'center';
            demoMsg.style.borderRadius = '10px';
            demoMsg.style.marginTop = '2rem';
            demoMsg.innerHTML = `
                <h3>${section} Module</h3>
                <p>This is a demonstration of the ${section.toLowerCase()} management module.</p>
                <p>In the full version, you would be able to:</p>
                <ul style="text-align: left; display: inline-block; margin-top: 1rem;">
                    <li>Add, edit, and delete ${section.toLowerCase()} records</li>
                    <li>View detailed information</li>
                    <li>Generate reports</li>
                    <li>Export data</li>
                </ul>
            `;
            dashboardContent.appendChild(demoMsg);
        }
    }
}

// Chart initialization (would be used with a chart library)
function initializeCharts() {
    // This would initialize charts using Chart.js or similar
    console.log('Charts would be initialized here');
}

// Data export functionality
function exportData(format) {
    alert(`Exporting data in ${format} format...\nThis would download a file in production.`);
}
