from bball.space import Space, AddableObject


def create_space(*objs: AddableObject) -> Space:
    return Space().add(*objs)
