from app.extensions import db
from app.models.room import Room
from app.models.block import Block


class RoomService:

    @staticmethod
    def create_room(
        block_id,
        room_number,
        floor,
        capacity,
        occupied=0,
        status="Available"
    ):
        block = db.session.get(Block, block_id)

        if not block:
            raise ValueError("Block not found")

        if occupied > capacity:
            raise ValueError(
                "Occupied spaces cannot exceed room capacity"
            )

        existing_room = Room.query.filter_by(
            block_id=block_id,
            room_number=room_number
        ).first()

        if existing_room:
            raise ValueError(
                "A room with this number already exists in this block"
            )

        room = Room(
            block_id=block_id,
            room_number=room_number,
            floor=floor,
            capacity=capacity,
            occupied=occupied,
            status=status
        )

        db.session.add(room)
        db.session.commit()

        return room

    @staticmethod
    def get_all_rooms():
        return Room.query.order_by(Room.id.asc()).all()

    @staticmethod
    def get_room_by_id(room_id):
        return db.session.get(Room, room_id)

    @staticmethod
    def get_rooms_by_block(block_id):
        block = db.session.get(Block, block_id)

        if not block:
            raise ValueError("Block not found")

        return Room.query.filter_by(
            block_id=block_id
        ).order_by(Room.id.asc()).all()

    @staticmethod
    def update_room(room_id, data):
        room = db.session.get(Room, room_id)

        if not room:
            raise ValueError("Room not found")

        if "block_id" in data:
            block = db.session.get(
                Block,
                data["block_id"]
            )

            if not block:
                raise ValueError("Block not found")

            room.block_id = data["block_id"]

        if "room_number" in data:
            room.room_number = data["room_number"]

        if "floor" in data:
            room.floor = data["floor"]

        if "capacity" in data:
            room.capacity = data["capacity"]

        if "occupied" in data:
            room.occupied = data["occupied"]

        if room.occupied > room.capacity:
            raise ValueError(
                "Occupied spaces cannot exceed room capacity"
            )

        if "status" in data:
            room.status = data["status"]

        db.session.commit()

        return room

    @staticmethod
    def delete_room(room_id):
        room = db.session.get(Room, room_id)

        if not room:
            raise ValueError("Room not found")

        db.session.delete(room)
        db.session.commit()

        return True