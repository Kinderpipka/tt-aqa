from typing import Any

from faker import Faker

from schemas.post import PostCreate

fake = Faker()


def generate_post_data() -> PostCreate:
    return PostCreate(
        title=fake.sentence(nb_words=6),
        body=fake.paragraph(nb_sentences=3),
        userId=fake.random_int(min=1, max=10),
    )


def generate_user_data() -> dict[str, Any]:
    return {
        "name": fake.name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "zipcode": fake.zipcode(),
        },
    }
