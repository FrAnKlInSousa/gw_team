from sqlalchemy.ext.asyncio import AsyncSession
from gw_team.database

async def create_user():
    async with AsyncSession(engine, expire_on_commit=False) as session:
    user_db = await session.scalar(
        select(User).where(User.email == user.email)
    )
    if user_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='email já existe.'
        )

    modalities_obj = await session.scalars(
        select(Modality).where(Modality.name.in_(user.modalities))
    )

    modalities = modalities_obj.all()

    user_db = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        last_name=user.last_name,
        user_type=user.user_type,
    )
    for modality in modalities:
        assoc = UserModality(
            user=user_db,
            modality=modality,
            start_date=datetime.now(),
        )
        user_db.modalities_assoc.append(assoc)

    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    await session.execute(
        select(User)
        .where(User.id == user_db.id)
        .options(
            selectinload(User.modalities_assoc).selectinload(
                UserModality.modality
            )
        )
    )