from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import os
from utils.log_file import log_event
from utils.caching import cache_results, get_cached_results

def create_search_index(index_dir, root_dir):
    schema = Schema(file_path=ID(stored=True), content=TEXT(stored=True))
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    ix = create_in(index_dir, schema)
    writer = ix.writer()
    system_files = ['DumpStack.log.tmp', 'hiberfil.sys', 'pagefile.sys', 'swapfile.sys']
    system_dirs = [os.path.join(root_dir, 'Windows'), os.path.join(root_dir, 'System32')]

    for root, dirs, files in os.walk(root_dir):
        # Skip system directories
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in system_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            if file in system_files:
                log_event('INFO', f"Skipping {file_path}: Known system file")
                continue
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                log_event('INFO', f"Indexing {file_path}")
                writer.add_document(file_path=file_path, content=content)
            except PermissionError:
                log_event('WARNING', f"Skipping {file_path}: Permission denied")
            except Exception as e:
                log_event('ERROR', f"Could not read {file_path}: {e}")
    writer.commit()
    log_event('INFO', f"Index created successfully in {index_dir}")

def search_files(index_dir, query_str):
    log_event('INFO', f"Searching for '{query_str}' in {index_dir}")
    cached_results = get_cached_results(query_str)
    if cached_results:
        log_event('INFO', f"Cache hit for query '{query_str}'")
        print(f"Cached results: {cached_results}")
        return cached_results
    else:
        log_event('INFO', f"Cache miss for query '{query_str}'")

    ix = open_dir(index_dir)
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        log_event('INFO', f"Found {len(results)} result(s) for query '{query_str}'")
        result_list = [result['file_path'] for result in results]
        for result in results:
            #log_event('INFO', f"Found: {result['file_path']}")
            print(f"Found: {result['file_path']}")
            #(snippet: {result.highlights('content')})
        cache_results(query_str, ', '.join(result_list))
        return result_list
