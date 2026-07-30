from app.extensions import db
from app.models.block import Block


class BlockService:

    @staticmethod
    def create_block(name, gender):
        existing_block = Block.query.filter_by(
            name=name
        ).first()

        if existing_block:
            raise ValueError("A block with this name already exists")

        block = Block(
            name=name,
            gender=gender
        )

        db.session.add(block)
        db.session.commit()

        return block

    @staticmethod
    def get_all_blocks():
        return Block.query.order_by(Block.id.asc()).all()

    @staticmethod
    def get_block_by_id(block_id):
        return db.session.get(Block, block_id)

    @staticmethod
    def update_block(block_id, data):
        block = db.session.get(Block, block_id)

        if not block:
            raise ValueError("Block not found")

        if "name" in data:
            existing_block = Block.query.filter(
                Block.name == data["name"],
                Block.id != block_id
            ).first()

            if existing_block:
                raise ValueError(
                    "A block with this name already exists"
                )

            block.name = data["name"]

        if "gender" in data:
            block.gender = data["gender"]

        db.session.commit()

        return block

    @staticmethod
    def delete_block(block_id):
        block = db.session.get(Block, block_id)

        if not block:
            raise ValueError("Block not found")

        db.session.delete(block)
        db.session.commit()

        return True