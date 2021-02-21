const Joi = require("@hapi/joi");
const { createJsonWebToken, cookieConfig } = require("./auth");

const usersDatabase = [
	{
		name: "A User",
		email: "user@example.com",
		scope: ["user"],
	},
	{
		name: "An Owner",
		email: "owner@example.org",
		scope: ["owner", "moderator"],
	},
	{
		name: "An Admin",
		email: "admin@example.net",
		scope: ["admin", "secret"],
	},
];

let statusDatabase = {
	status: "prevote",
	time: "YYYY-MM-DD",
};

let statusRoll = {
	a: false,
	b: true,
	c: true,
};

module.exports = [
	{
		method: "POST",
		path: "/session",
		options: {
			validate: {
				payload: Joi.object({
					email: Joi.string().email().required(),
					password: Joi.string().required(),
				}),
			},
		},
		handler: async (request, h) => {
			const { email, password } = request.payload;
			const user = usersDatabase.find((u) => u.email === email);

			if (password === "user123") {
				const jwt = await createJsonWebToken(user);
				return h
					.response()
					.state("my-jwt", jwt, cookieConfig)
					.code(201);
			}

			return h.response().code(401);
		},
	},
	{
		method: "DELETE",
		path: "/session",
		handler: (request, h) => h
			.response()
			.unstate("my-jwt", cookieConfig)
			.code(200),
	},
	{
		method: "GET",
		path: "/whoami",
		handler: (request, h) => request.auth.credentials,
	},
	{
		method: "GET",
		path: "/status",
		handler: () => statusDatabase,
	},
	{
		method: "PATCH",
		path: "/status",
		handler: (request, h) => {
			const { phase, date } = request.payload;
			// if (request.auth.credentials) {
			statusDatabase = {
				status: phase,
				time: date,
			};
			return h.response().code(200);
			// }
			// return h.response().code(401);
		},
	},
	{
		method: "GET",
		path: "/roll",
		handler: () => statusRoll,
	},
	{
		method: "PATCH",
		path: "/roll",
		handler: (request, h) => {
			const { a, b, c } = request.payload;
			// if (request.auth.credentials) {
			statusRoll = {
				a: a,
				b: b,
				c: c
			};
			return h.response().code(200);
			// }
			// return h.response().code(401);
		},
	},
];
