def first_node_or_none(nodes):
    return next(iter(nodes), None)


def try_get_text(node):
    if isinstance(node, list):
        if len(node) > 0:
            return node[0].text.strip()
    elif node:
        return node.text.strip()

    return ""


def try_get_text_from_nodes(nodes):
    text = list()

    for n in nodes:
        text.append(try_get_text(n))

    return text


def class_contains(tag, string):
    return tag.has_attr("class") \
        and string in tag["class"]


def href_contains(tag, string):
    return tag.has_attr("href") \
        and string in tag["href"]
