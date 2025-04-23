document.addEventListener('DOMContentLoaded', () => {
    const daysGrid = document.getElementById('days-grid');
    const monthYear = document.getElementById('month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
  
    let currentDate = new Date();

    function renderCalendar() {
      const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
      const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
      const daysInMonth = lastDay.getDate();
      const startDay = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1; // Пн=0, Вс=6
  
      monthYear.textContent = new Intl.DateTimeFormat('ru-RU', {
        month: 'long',
        year: 'numeric'
      }).format(currentDate);
  
      daysGrid.innerHTML = '';
  
      // Пустые ячейки для дней предыдущего месяца
      for (let i = 0; i < startDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.classList.add('other-month');
        daysGrid.appendChild(emptyDay);
      }
  
      // Ячейки текущего месяца
      const today = new Date();
      for (let i = 1; i <= daysInMonth; i++) {
        const day = document.createElement('div');
        day.textContent = i;

        if (
          currentDate.getMonth() === today.getMonth() &&
          currentDate.getFullYear() === today.getFullYear() &&
          i === today.getDate()
        ) {
          day.classList.add('today');
        }
        
        daysGrid.appendChild(day);
      }
    }
  
    prevMonthBtn.addEventListener('click', () => {
      currentDate.setMonth(currentDate.getMonth() - 1);
      renderCalendar();
    });
  
    nextMonthBtn.addEventListener('click', () => {
      currentDate.setMonth(currentDate.getMonth() + 1);
      renderCalendar();
    });
  
    renderCalendar();
  });