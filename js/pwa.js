// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('ServiceWorker registration successful');
            })
            .catch(err => {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}

// PWA Install Prompt
let deferredPrompt;
const installButton = document.getElementById('installButton');

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show the install button
    installButton.style.display = 'block';
    
    installButton.addEventListener('click', () => {
        // Hide the install button
        installButton.style.display = 'none';
        // Show the install prompt
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        deferredPrompt.userChoice.then((choiceResult) => {
            if (choiceResult.outcome === 'accepted') {
                console.log('User accepted the install prompt');
            } else {
                console.log('User dismissed the install prompt');
            }
            deferredPrompt = null;
        });
    });
});

// Detect if app is installed
window.addEventListener('appinstalled', (evt) => {
    console.log('App was installed successfully');
    installButton.style.display = 'none';
});

// Check if app is running in standalone mode (installed)
if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('Running in standalone mode');
    installButton.style.display = 'none';
}
