// Create and inject menu and styles dynamically
document.addEventListener('DOMContentLoaded', () => {

    //document.head.appendChild(style);
  
    // Create menu
    const nav = document.createElement('nav');
    const content = document.createElement('div');
    content.id = 'content';
  
    const menuItems = [
      { name: 'Climate', file: 'climate' },
      { name: 'Rules', file: 'rules' },      
      { name: 'Relais', file: 'relays' }
    ];
  
    menuItems.forEach((item, index) => {
      const btn = document.createElement('button');
      if(location.href.includes(item.file)) {
        console.log('active', item.file);
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
      btn.textContent = item.name;
      btn.addEventListener('click', () => {
        location.href = item.file;
        //loadContent(item.file);
        //setActive(btn);
      });
      
      nav.appendChild(btn);
    });
  
    document.body.prepend(content);
    document.body.prepend(nav);
  });