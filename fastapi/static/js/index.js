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