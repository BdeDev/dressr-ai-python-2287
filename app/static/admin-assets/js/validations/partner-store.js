$("#add-partner-store").validate({
	ignore: [],
	rules: {
		name: {
			required: true,
			},
		website: {
			required: true,
			},
		logo: {
			required: true,
			},
		},
	messages: {
		name: {
			required: "Please Enter Name",
			},
		website: {
			required: "Please Enter Website",
			},

		logo: {
			required: "Please upload logo",
			},
		},
	});  


$("#edit-partner-store").validate({
	ignore: [],
        rules: {
            name: {
                required: true,
                },
            website: {
                required: true,
                },
            logo: {
                required: true,
                },
            },
        messages: {
            name: {
                required: "Please Enter Name",
                },
            website: {
                required: "Please Enter Website",
                },

            logo: {
                required: "Please upload logo",
                },
            },
    });