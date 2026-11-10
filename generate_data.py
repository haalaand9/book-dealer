from datetime import date, timedelta
import json
import random

random.seed(42)

books = [
    {"id": "B001", "title": "The Silent Orchard", "author": "Leah Martin", "genre": "Fiction", "price": 18.99},
    {"id": "B002", "title": "Night Flight to Lisbon", "author": "Daniel Kline", "genre": "Adventure", "price": 21.5},
    {"id": "B003", "title": "The Hollow Clock", "author": "Mira Sol", "genre": "Mystery", "price": 19.25},
    {"id": "B004", "title": "Paper Lanterns", "author": "Ari Bennett", "genre": "Historical", "price": 22.0},
    {"id": "B005", "title": "The Last Mapmaker", "author": "Nora Wren", "genre": "Fantasy", "price": 20.75},
    {"id": "B006", "title": "Wildflower Roads", "author": "Elsie Harrow", "genre": "Romance", "price": 17.5},
    {"id": "B007", "title": "Cinder Harbor", "author": "Joel Pierce", "genre": "Mystery", "price": 18.0},
    {"id": "B008", "title": "The Blue Hour", "author": "Tara Monroe", "genre": "Drama", "price": 24.0},
    {"id": "B009", "title": "Glass and Ash", "author": "Evan Cole", "genre": "Speculative", "price": 23.25},
    {"id": "B010", "title": "Orchid House", "author": "Renee Huxley", "genre": "Literary", "price": 19.5},
    {"id": "B011", "title": "Midnight Signal", "author": "Lucas Green", "genre": "Thriller", "price": 20.99},
    {"id": "B012", "title": "The Quiet Tide", "author": "Makenna Ross", "genre": "Contemporary", "price": 18.75},
    {"id": "B013", "title": "Velvet Sun", "author": "Sofia James", "genre": "Romance", "price": 17.0},
    {"id": "B014", "title": "Winter in Briar", "author": "Elliot Ward", "genre": "Historical", "price": 21.25},
    {"id": "B015", "title": "Ashes of Cobalt", "author": "Marin Vale", "genre": "Fantasy", "price": 22.5},
    {"id": "B016", "title": "The Fifth Ember", "author": "J. Carter", "genre": "Sci-Fi", "price": 25.0},
    {"id": "B017", "title": "Saltwater Letters", "author": "Ivy Morrow", "genre": "Drama", "price": 16.99},
    {"id": "B018", "title": "Pine & Stone", "author": "Hannah North", "genre": "Fiction", "price": 19.0},
    {"id": "B019", "title": "Crown of Thornes", "author": "Kendra Pike", "genre": "Fantasy", "price": 24.5},
    {"id": "B020", "title": "The River Between", "author": "Oscar Vale", "genre": "Literary", "price": 18.25},
    {"id": "B021", "title": "Starlight Atlas", "author": "Piper Gray", "genre": "Sci-Fi", "price": 21.75},
    {"id": "B022", "title": "The Chapel Key", "author": "Cora Fenn", "genre": "Mystery", "price": 19.75},
    {"id": "B023", "title": "Harbor of Echoes", "author": "Noah Raines", "genre": "Adventure", "price": 22.25},
    {"id": "B024", "title": "Tomorrow's Orchard", "author": "Mila Stone", "genre": "Nonfiction", "price": 26.0},
    {"id": "B025", "title": "Field Notes for Believers", "author": "Gavin Cross", "genre": "Nonfiction", "price": 24.75},
    {"id": "B026", "title": "Copper Lanterns", "author": "Rebecca Dale", "genre": "Historical", "price": 20.25},
    {"id": "B027", "title": "The Borrowed Sky", "author": "Adrian Shaw", "genre": "Fantasy", "price": 21.0},
    {"id": "B028", "title": "Beneath the Willow", "author": "Clara West", "genre": "Romance", "price": 17.75},
    {"id": "B029", "title": "Crimson Ledger", "author": "Dylan Hill", "genre": "Thriller", "price": 23.5},
    {"id": "B030", "title": "The Light at Dune Point", "author": "Vivian Frost", "genre": "Adventure", "price": 18.5},
    {"id": "B031", "title": "Keeping the Dawn", "author": "Julia Hallow", "genre": "Fiction", "price": 19.99},
    {"id": "B032", "title": "Sweetwater Summer", "author": "Mason Bell", "genre": "Romance", "price": 16.5},
    {"id": "B033", "title": "Braided Memory", "author": "Samantha Reed", "genre": "Drama", "price": 18.99},
    {"id": "B034", "title": "A Wake of Birds", "author": "Winston Hale", "genre": "Literary", "price": 20.5},
    {"id": "B035", "title": "Morrow's Thread", "author": "Alina Brooks", "genre": "Fantasy", "price": 21.5},
    {"id": "B036", "title": "White Chapel", "author": "Nina Moss", "genre": "Mystery", "price": 18.25},
    {"id": "B037", "title": "The Last Passenger", "author": "Simon Reed", "genre": "Thriller", "price": 22.75},
    {"id": "B038", "title": "The Wren and the Oak", "author": "Daphne Rowan", "genre": "Contemporary", "price": 17.5},
    {"id": "B039", "title": "Lanterns Over Gable", "author": "Martha Quinn", "genre": "Historical", "price": 23.0},
    {"id": "B040", "title": "Under the Ice Blue Sky", "author": "Aiden Brooks", "genre": "Adventure", "price": 19.25},
    {"id": "B041", "title": "Paper Crown", "author": "Harper Moss", "genre": "Drama", "price": 18.0},
    {"id": "B042", "title": "The Time Between Maps", "author": "Lena Pike", "genre": "Speculative", "price": 23.99},
    {"id": "B043", "title": "Mercury House", "author": "Theo Hart", "genre": "Sci-Fi", "price": 24.25},
    {"id": "B044", "title": "A Place for Echoes", "author": "Eliana Quill", "genre": "Fiction", "price": 18.5},
    {"id": "B045", "title": "Velvet Mirror", "author": "Jade Camden", "genre": "Mystery", "price": 19.5},
    {"id": "B046", "title": "Song of the Black Swan", "author": "Gwen Ellis", "genre": "Fantasy", "price": 22.0},
    {"id": "B047", "title": "Wild Cedar", "author": "Harlan Dorsey", "genre": "Nonfiction", "price": 25.5},
    {"id": "B048", "title": "The Last Winter of Faye", "author": "Celine Hart", "genre": "Literary", "price": 20.0},
    {"id": "B049", "title": "Broken Inkwell", "author": "Nadia Lowe", "genre": "Drama", "price": 17.99},
    {"id": "B050", "title": "The Bright Hour", "author": "Milo Ash", "genre": "Contemporary", "price": 18.75},
    {"id": "B051", "title": "The Stolen Orchard", "author": "Charlie Nix", "genre": "Historical", "price": 21.5},
    {"id": "B052", "title": "Seaward Fire", "author": "Janelle Cross", "genre": "Adventure", "price": 22.5},
    {"id": "B053", "title": "North of the Ashes", "author": "Nolan Pike", "genre": "Thriller", "price": 20.99},
    {"id": "B054", "title": "Quiet Bloom", "author": "Rhea Stone", "genre": "Romance", "price": 16.75},
    {"id": "B055", "title": "House of Larkspur", "author": "Evelyn Cross", "genre": "Fiction", "price": 18.25},
    {"id": "B056", "title": "The Distant Tide", "author": "Samir Vale", "genre": "Drama", "price": 19.0},
    {"id": "B057", "title": "Ashen Moss", "author": "Tessa Quill", "genre": "Fantasy", "price": 21.5},
    {"id": "B058", "title": "Whispers in Glass", "author": "Hugo Bloom", "genre": "Mystery", "price": 20.25},
    {"id": "B059", "title": "The Ember Atlas", "author": "Cora Dune", "genre": "Sci-Fi", "price": 24.0},
    {"id": "B060", "title": "The Cinder Archive", "author": "Marcus Flint", "genre": "Speculative", "price": 21.99},
]

def generate_history():
    today = date.today()
    purchases = []

    for book in books:
        popularity = {
            "Mystery": 18,
            "Fantasy": 16,
            "Romance": 14,
            "Sci-Fi": 15,
            "Thriller": 17,
            "Adventure": 14,
            "Historical": 12,
            "Fiction": 11,
            "Drama": 10,
            "Literary": 9,
            "Contemporary": 8,
            "Speculative": 12,
            "Nonfiction": 10,
        }.get(book["genre"], 8)

        for offset in range(5):
            day = today - timedelta(days=4 - offset)
            wave = random.randint(-4, 6)
            daily_sales = max(1, popularity + wave + (offset == 4) * 4 + (offset == 0) * 2)
            for _ in range(daily_sales):
                purchases.append({
                    "bookId": book["id"],
                    "date": day.isoformat(),
                    "quantity": 1,
                })

    return purchases

payload = {
    "generatedAt": date.today().isoformat(),
    "windowDays": 5,
    "books": books,
    "purchases": generate_history(),
}

with open("data/purchases.json", "w", encoding="utf-8") as file:
    json.dump(payload, file, indent=2)
    file.write("\n")

print(f"Created {len(books)} books and {len(payload['purchases'])} purchase records.")
