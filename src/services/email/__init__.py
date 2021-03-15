import json
import asyncio
from os import getenv
from httpx import AsyncClient
from jinja2 import Environment, FileSystemLoader


""" To-Do: Implement asyncio.Lock() and LRU caches """

class sender():

    def __init__(self):
        
        """ Init MailGun API wrapper """
        self.sender_name = getenv('MAIL_SENDER_NAME')
        self.sender_domain = getenv('MAIL_SENDER_DOMAIN')
        self.client = AsyncClient(
            auth = ("api", getenv('MAILGUN_PRIVATE_KEY')),
            base_url = f"https://api.mailgun.net/v3/{self.sender_domain}"
        )
        
        """ Init Jinja2 template system """
        self.templates = "./src/services/email/templates"
        self.env = Environment(
            loader=FileSystemLoader(searchpath=self.templates)
        )


    async def request(self, recipient: str, subject: str, content: str) -> None:
        
        await self.client.post(
            "/messages",
            data = {
                "from": f"{self.sender_name} <mailgun@{self.sender_domain}>",
                "to": recipient,
                "subject": subject,
                "html": content
            }
        )


    def load_template(self, case: str, values: dict) -> str:

        data = json.load(open(f"{self.templates}/data/{case}.json"))
        data.update(values)
        return self.env.get_template(f"{case}.html").render(data)


    async def on_register(self, values: dict) -> None:
        
        recipient = values["email"]
        subject = f"¡Registro exitoso!"
        content = self.load_template("register", values)
        await self.request(recipient, subject, content)


    async def on_verification(self, values: dict) -> None:
        
        recipient = values["email"]
        subject = f"Verificación de tu cuenta"
        content = self.load_template("verify", values)
        await self.request(recipient, subject, content)


    async def on_recovery(self, values: dict) -> None:
        
        recipient = values["email"]
        subject = f"Recuperación de tu cuenta"
        content = self.load_template("recovery", values)
        await self.request(recipient, subject, content)
