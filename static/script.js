document.addEventListener("DOMContentLoaded", () => {
    // Определение времени суток
    const hour = new Date().getHours();
    let timeOfDay = "Ночь";
    if (hour >= 6 && hour < 12) timeOfDay = "Утро";
    else if (hour >= 12 && hour < 18) timeOfDay = "День";
    else if (hour >= 18 && hour < 22) timeOfDay = "Вечер";
    document.getElementById("timeOfDay").textContent = `Сейчас: ${timeOfDay}`;
  
    fetchCocktails();
  });
  
  async function fetchCocktails() {
    const container = document.getElementById("cocktailList");
    try {
      const res = await fetch("/api/cocktails");
      const images = await res.json();
  
      images.forEach(src => {
        const fileName = decodeURIComponent(src.split('/').pop().replace(/\.[^/.]+$/, ''));
        const [name, price] = fileName.split('_');
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
          <img src="${src}" alt="${name}">
          <h3>${name}</h3>
          <p>${price} ₽</p>
        `;
        container.appendChild(card);
      });
    } catch (err) {
      container.innerHTML = "<p>Ошибка загрузки коктейлей</p>";
      console.error(err);
    }
  }
  