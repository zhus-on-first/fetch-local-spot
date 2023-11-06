      // Fetch location features by location_id
      const [selectedLocation, setSelectedLocation] = useState("")

      useEffect(() => {
        const fetchFeatures = async () => {
            console.log("Selected Location:", selectedLocation);
            if (selectedLocation) {
                const featureResponse = await fetch(`/location/<int:location_id>/features`)
                if (featureResponse.ok) {
                    const featureData = await featureResponse.json()
                    setFormData(prev => ({ ...prev, features: featureData}))
                } else {
                    const errorMessages = await featureResponse.json();
                    setErrors(errorMessages.errors);
                }
            }
        }
        fetchFeatures()
      }, [selectedLocation])
    