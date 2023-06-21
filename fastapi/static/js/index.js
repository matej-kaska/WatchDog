const addWebsite = async (website) => {
    try {
      const rawResponse = await fetch('http://localhost:5001/add-website', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ hostname: website })
      });

      if (rawResponse.status === 400) {
        const content = await rawResponse.json();
        if (content.message === "Wrong url!") {
            window.alert("URL odkaz neexistuje nebo nefunguje!")
        }
        else if (content.message === "Couldn't get IP from website!") {
            window.alert("Nelze získat IP adresu serveru!")
        }
        else if (content.message === "Something went wrong!") {
            window.alert("Něco se pokazilo!")
        }
      }

      if (rawResponse.status === 201) {
        location.reload();
      }
  
    } catch (error) {
      console.error(error);
    }
};

const CheckStatus = async (ip) => {
    try {
        const rawResponse = await fetch('http://localhost:5001/check-status', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ ip: ip })
        });
        const content = await rawResponse.json();
        if (rawResponse.status === 400) {
            if (content.message === "Something went wrong!") {
                window.alert("Něco se pokazilo!")
            }
        }
        else if (rawResponse.status === 200) {
            document.getElementById(ip + "code").innerHTML = content.status;
            document.getElementById(ip + "chec").innerHTML = content.date;
        }

      } catch (error) {
        console.error(error);
      }
    };

// Chart for website
const ctx = document.getElementById('StatusChart');

const data = {
  datasets: [
    {
      data: chart_data,
      borderColor: "#00FF00",
      backgroundColor: "rgba(0,255,0,0.3)",
      fill: "start",
      label: "Status",
      pointBackgroundColor: function(context) {
        var value = context.dataset.data[context.dataIndex].y;
        if (value === 'DOWN') return "red";
        return "#00FF00";
      },
      pointBorderColor: function(context) {
        var value = context.dataset.data[context.dataIndex].y;
        if (value === 'DOWN') return "red";
        return "#00FF00";
      }
    }
  ]
};

new Chart(ctx, {
  type: 'line',
  data: data,
  options: {
    plugins: {
      filler: {
        propagate: false,
      },
      title: {
        display: true,
        text: "Status of the website"
      },
      tooltip: {
        displayColors: false,
        callbacks: {
          title: function(context) {
            return context[0].formattedValue
          },
          label: function(context) {
            return moment(context.label).format('D.M.YYYY HH:mm:ss');
          }
        }
      }
    },
    interaction: {
      intersect: false,
    },
    scales: {
      y: {
        type: 'category',
        labels: ['UP', 'DOWN'],
      },
      x: {
        ticks: {
          callback: function(val, index) {
            if (index % 3 === 0) {
              return moment(this.getLabelForValue(val), 'YYYY-MM-DD HH:mm:ss').format('D.M.');
            }
            return '';
          }
        }
      }
    }
  },
});