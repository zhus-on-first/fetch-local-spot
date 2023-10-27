    useEffect(() => {
        const fetchReports = async () => {
          const response = await fetch("/reports");
          if (response.ok) {
            const data = await response.json();
            setReports(data);
          } else {
                const errorMessages = await response.json();
                setErrors(errorMessages.errors)
            }
        }
        fetchReports();
      }, []);
    

    const handleNewReport = (newReport) => {
        setReports([...reports, newReport]);
        setConfirmationMessage("Report submitted successfully!");
      };


                <h2>Existing Reports</h2>
          <ul>
            {reports.map((report, index) => (
                <li key={index}>
                <p>insert report details here</p>
                </li>
            ))}
          </ul>
    
          <h2>Submit a New Report</h2>
          <NewReportForm handleNewReport={handleNewReport} />