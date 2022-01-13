from ctk_cli import CLIArgumentParser
import girder_client
import os


def descend_folder(gc, folder_id, verbose=True):
    #Recursively descend into folders, finding slides and other folders
    
    #recursively call on subfolders
    for folder in gc.listFolder(parentId=folder_id, parentFolderType='folder',
                                limit=None):
        descend_folder(gc, folder['_id'], verbose=True)
        
    #get list of slides in current folder
    for slide in gc.listItem(folderId=folder_id, limit=None):
        query_slide(gc, slide['_id'], verbose)

    return


def query_slide(gc, slide_id, verbose=True):
    #Get basic properties of the slide and post as metadata
    
    #get large_image properties of slide
    properties = gc.get('/item/%s/tiles' % slide_id)
    
    if verbose:
        print('Getting properties from slide %s' % (slide_id))

    #copy properties to metadata - in reality we can create a dict with a 'histoqc' key and assign 
    #another dict of metadata properties to this. {'histoqc': histoqc_results_dict}
    gc.addMetadataToItem(slide_id, properties)

    return


def parse_dir_input(directory):
    #Parses girder ID out of directory argument passed to CLI

    return directory.split(os.sep)[4]


def main(args):
    """We expect to receive a girder ID of a folder (directory), a Girder API url (girderApiUrl),
    and a Girder token (girderToken). We use the Girder API to walk the folders recursively,
    acquiring info from each item/slide, and writing metadata back to the items.
    """

    #create girder client from token and url
    gc = girder_client.GirderClient(apiUrl=args.girderApiUrl)
    gc.setToken(args.girderToken)

    #descend recursively into folders and analyze each slide within
    descend_folder(gc, parse_dir_input(args.directory))


if __name__ == '__main__':
    main(CLIArgumentParser().parse_args())
