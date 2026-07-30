from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.block_schema import (
    BlockSchema,
    BlockUpdateSchema
)

from app.services.block_service import BlockService


block_schema = BlockSchema()
block_update_schema = BlockUpdateSchema()


def create_block():

    try:
        data = block_schema.load(
            request.get_json()
        )

        block = BlockService.create_block(
            name=data["name"],
            gender=data["gender"]
        )

        return jsonify({
            "message": "Block created successfully",
            "block": block.to_dict()
        }), 201

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 409

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_all_blocks():

    try:
        blocks = BlockService.get_all_blocks()

        return jsonify({
            "blocks": [
                block.to_dict()
                for block in blocks
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def get_block(block_id):

    try:
        block = BlockService.get_block_by_id(
            block_id
        )

        if not block:
            return jsonify({
                "error": "Block not found"
            }), 404

        return jsonify({
            "block": block.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def update_block(block_id):

    try:
        data = block_update_schema.load(
            request.get_json()
        )

        block = BlockService.update_block(
            block_id,
            data
        )

        return jsonify({
            "message": "Block updated successfully",
            "block": block.to_dict()
        }), 200

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


def delete_block(block_id):

    try:
        BlockService.delete_block(
            block_id
        )

        return jsonify({
            "message": "Block deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500