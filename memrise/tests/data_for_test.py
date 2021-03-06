from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity

fresh_course_entities = [
    CourseEntity(
        id=1987730,
        name="Adjective Complex",
        url="/course/1987730/adjective-complex/",
        difficult=6,
        num_words=19,
        num_levels=7,
        difficult_url="/course/1987730/adjective-complex/difficult-items/",
    ),
    CourseEntity(
        id=2147115,
        name="Verbs New Name verb of clothes",
        url="/course/2147115/verbs-of-wear-clothes/",
        difficult=5,
        num_words=19,
        num_levels=2,
        difficult_url="/course/2147115/verbs-of-wear-clothes/difficult-items/",
    ),
    CourseEntity(
        id=1234,
        name="New Course",
        url="/course/1234/new-courses/",
        difficult=5,
        num_words=3,
        num_levels=2,
        difficult_url="/course/1234/new-courses/difficult-items/",
    ),
    CourseEntity(
        id=5605650,
        name="Animals",
        url="/course/5605650/animals/",
        difficult=1,
        num_words=8,
        num_levels=3,
        difficult_url="/course/5605650/animals/difficult-items/",
    ),
]

fresh_level_entities = [
    LevelEntity(
        id=1,
        number=1,
        course_id=1987730,
        name="New level",
        words=[WordEntity(id=1, word_a="test", word_b="sdlfksjd", level_id=1)],
    ),
    LevelEntity(
        id=2,
        number=2,
        course_id=1987730,
        name="New level",
        words=[WordEntity(id=2, word_a="check", word_b="blah-blah", level_id=2)],
    ),
    LevelEntity(id=3, number=3, course_id=1987730, name="New level"),
    LevelEntity(id=52, number=1, course_id=2147115, name="New level"),
    LevelEntity(id=137, number=1, course_id=5605650, name="Level 123-346"),
    LevelEntity(id=138, number=2, course_id=5605650, name="New level"),
    LevelEntity(id=1273, number=12, course_id=5605650, name="New level12"),
    LevelEntity(id=3638, number=11, course_id=2147115, name="New level11"),
]

fresh_word_entities = [
    WordEntity(id=1, word_a="nasty", word_b="мерзкий, противный, неприятный", level_id=1),
    WordEntity(id=2, word_a="rough", word_b="грубый", level_id=1),
    WordEntity(id=3, word_a="tense", word_b="напряженный", level_id=1),
    WordEntity(id=4, word_a="vital", word_b="жизненно важный", level_id=1),
    WordEntity(
        id=5, word_a="deprecated", word_b="устаревший, исключенный, не рекомендуемый", level_id=1),
    WordEntity(id=6, word_a="joyful", word_b="радостный, ликующий", level_id=1),
    WordEntity(id=7, word_a="startled", word_b="испуганный, пораженный, встревоженный", level_id=1),
    WordEntity(id=8, word_a="humiliated", word_b="униженный", level_id=1),
    WordEntity(id=9, word_a="remarkable", word_b="замечательный, выдающийся", level_id=1),
    WordEntity(id=10, word_a="odd", word_b="странный, необычный", level_id=1),
    WordEntity(
        id=11, word_a="awkward", word_b="неловкий, неуклюжий (момент, поведение)", level_id=1
    ),
    WordEntity(id=12, word_a="mere", word_b="простой, всего лишь", level_id=1),
    WordEntity(id=13, word_a="pleased", word_b="довольный", level_id=1),
    WordEntity(id=14, word_a="familiar", word_b="привычный, знакомый", level_id=1),
    WordEntity(id=15, word_a="certain", word_b="определенный, уверенный", level_id=1),
    WordEntity(id=16, word_a="essential", word_b="существенный, обязательный (вещь)", level_id=1),
    WordEntity(id=17, word_a="immediate", word_b="немедленный", level_id=1),
    WordEntity(id=18, word_a="appropriate", word_b="соответствующий, подходящий", level_id=1),
    WordEntity(id=19, word_a="irregular", word_b="неправильный, нестандартный", level_id=1),
    WordEntity(id=20, word_a="to adjust", word_b="регулировать, приспосабливаться", level_id=1),
    WordEntity(id=204850790, word_a="fair", word_b="справедливый, честный", level_id=1),
    WordEntity(id=204850795, word_a="nasty", word_b="мерзкий, противный, неприятный", level_id=1),
    WordEntity(id=204850798, word_a="rough", word_b="грубый", level_id=1),
    WordEntity(id=204850807, word_a="vital", word_b="жизненно важный", level_id=1),
    WordEntity(id=204850898, word_a="irregular", word_b="неправильный, нестандартный", level_id=2),
    WordEntity(
        id=204850899, word_a="independent", word_b="независимый, самостоятельный", level_id=2
    ),
    WordEntity(id=204850900, word_a="proper", word_b="надлежащий, правильный", level_id=2),
    WordEntity(id=204857074, word_a="content", word_b="blah-blah", level_id=4),
    WordEntity(id=204857075, word_a="calm", word_b="blah-blah", level_id=4),
    WordEntity(id=204857126, word_a="terrified", word_b="blah-blah", level_id=3),
]