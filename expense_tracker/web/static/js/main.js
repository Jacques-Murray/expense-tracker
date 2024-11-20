// Main JavaScript functionality for Expense Tracker

// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    const quickAddForm = document.getElementById('quickAddForm');
    if (quickAddForm) {
        quickAddForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(quickAddForm);
            try {
                const response = await fetch(quickAddForm.action, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();
                if (result.success) {
                    // Refresh the page to show the new expense
                    window.location.reload();
                } else {
                    alert(result.message || 'Failed to add expense');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to add expense. Please try again.');
            }
        });
    }

    // Month navigation
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const currentMonthBtn = document.getElementById('currentMonth');

    if (prevMonthBtn && nextMonthBtn && currentMonthBtn) {
        let currentDate = new Date();

        prevMonthBtn.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            updateDashboard(currentDate);
        });

        nextMonthBtn.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            updateDashboard(currentDate);
        });

        currentMonthBtn.addEventListener('click', () => {
            currentDate = new Date();
            updateDashboard(currentDate);
        });
    }
});

// Update dashboard data
async function updateDashboard(date) {
    try {
        const response = await fetch(`/api/dashboard?date=${date.toISOString()}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Update month display
        const currentMonthBtn = document.getElementById('currentMonth');
        currentMonthBtn.textContent = date.toLocaleString('default', { month: 'long', year: 'numeric' });

        // Update chart
        const chart = Chart.getChart('monthlyChart');
        if (chart) {
            chart.data.labels = data.dates;
            chart.data.datasets[0].data = data.daily_expenses;
            chart.update();
        }

        // Update summary
        document.querySelector('#monthlyTotal').textContent = `$${data.monthly_total.toFixed(2)}`;
        document.querySelector('#dailyAverage').textContent = `$${data.daily_average.toFixed(2)}`;

        // Update progress bar
        const progressBar = document.querySelector('.progress-bar');
        progressBar.style.width = `${data.budget_percentage}%`;
        progressBar.textContent = `${data.budget_percentage}%`;

        // Update recent expenses table
        const tbody = document.querySelector('table tbody');
        tbody.innerHTML = data.recent_expenses.map(expense => `
            <tr>
                <td>${new Date(expense.date).toLocaleDateString()}</td>
                <td>
                    <span class="badge bg-${expense.category_color}">
                        ${expense.category}
                    </span>
                </td>
                <td>${expense.description}</td>
                <td class="text-end">$${expense.amount.toFixed(2)}</td>
            </tr>
        `).join('');

    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update dashboard. Please try again.');
    }
}

// Delete expense
async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }

    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        if (result.success) {
            window.location.reload();
        } else {
            alert(result.message || 'Failed to delete expense');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete expense. Please try again.');
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Handle expense filtering
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(filterForm);
            const params = new URLSearchParams(formData);
            window.location.href = `/expenses?${params.toString()}`;
        });
    }
});
