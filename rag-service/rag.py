    
class RAG:

    def build(self, data):

        questions = data.get(
            "data",
            []
        )

        texts = []

        for q in questions:

            if isinstance(q, dict):

                texts.append(
                    q.get(
                        "question",
                        ""
                    )
                )

        return len(texts)